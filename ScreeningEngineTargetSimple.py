"""
================================================================================
SYSTEM: AUTOMATED BULK SANCTIONS SCREENING ENGINE

DESCRIPTION:
This engine performs high-performance fuzzy matching between a proprietary
customer database and international sanctions lists (OpenSanctions TargetsSimple).
It utilizes a dual-model approach (Jaro-Winkler + Levenshtein) to identify
potential matches, aliases, and phonetic similarities while cross-referencing
secondary identifiers (Date of Birth and Country) to categorize risk levels.

COMPLIANCE NOTE:
The confidence levels (CRITICAL, HIGH, MEDIUM) are determined by a combination
of name similarity and attribute validation. "Medium" hits represent name-only
matches and require manual verification.
================================================================================
"""

import csv
import logging
import os
import json
from tqdm import tqdm

# ==============================================================================
# 1. RULE TUNING & RISK CONFIGURATION
# Adjust these variables to calibrate the sensitivity of the screening engine.
# ==========================================
# Global Thresholds
BASE_MATCH_THRESHOLD = 85.0  # Minimum score (0-100) to flag an alert for review
CRITICAL_MATCH_THRESHOLD = 90.0  # Score above which a hit is considered 'Critical'

# Fuzzy Model Weighting (Total must equal 1.0)
# Jaro-Winkler is weighted higher (0.7) to prioritize matching name prefixes.
JARO_WINKLER_WEIGHT = 0.17
LEVENSHTEIN_WEIGHT = 0.83

# Performance vs. Accuracy Balance
# Lower values increase speed but may miss long aliases or multi-part names.
NAME_LENGTH_TOLERANCE = 22

# Batching / Sampling (Set to None for production runs)
SCREEN_LIMIT = 50

# Infrastructure Paths
SANCTIONS_FILE = "TargetsSimple.csv"
CUSTOMER_FILE = "customers_core_export.csv"
OUTPUT_FILE = "screening_alerts.csv"
# ==============================================================================

# Attempt to initialize high-performance fuzzy library
try:
    from rapidfuzz import fuzz

    if hasattr(fuzz, 'jaro_winkler_similarity'):
        calc_jw = fuzz.jaro_winkler_similarity
    else:
        from rapidfuzz import distance

        calc_jw = distance.JaroWinkler.similarity
    HAS_RAPIDFUZZ = True
except (ImportError, AttributeError):
    import difflib

    HAS_RAPIDFUZZ = False
    import logging

    logging.getLogger(__name__).warning(
        "Performance Warning: rapidfuzz not found. Utilizing standard library fallback."
    )

# Logging configuration for audit trails
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def load_csv_data(filepath, description="CSV Data"):
    """
    Standardized loader for flat-file datasets.
    Includes error handling and progress tracking for large datasets.
    """
    if not os.path.exists(filepath):
        logger.error(f"IO Error: Reference file {filepath} missing.")
        return []

    data = []
    logger.info(f"INIT: Loading {description}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            total_rows = sum(1 for _ in f) - 1

        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, total=total_rows, desc=f"Importing {description}", unit=" rows"):
                data.append(dict(row))
        logger.info(f"SUCCESS: {len(data)} records imported.")
        return data
    except Exception as e:
        logger.error(f"CRITICAL: Failed to parse {filepath}. Details: {e}")
        return []


def calculate_weighted_score(name1, name2):
    """
    Core Logic: Combines Jaro-Winkler (prefix bias) and Levenshtein (edit distance).
    This provides a balanced score that accounts for both typos and name variations.
    """
    if not name1 or not name2: return 0
    n1, n2 = name1.lower().strip(), name2.lower().strip()

    if HAS_RAPIDFUZZ:
        jw = calc_jw(n1, n2) * 100
        lev = fuzz.ratio(n1, n2)
        return (jw * JARO_WINKLER_WEIGHT) + (lev * LEVENSHTEIN_WEIGHT)
    else:
        return difflib.SequenceMatcher(None, n1, n2).ratio() * 100


def screen_customers(customers, sanctions_list):
    """
    Primary Screening Loop.
    Matches every customer against the full sanctions list and performs
    secondary attribute validation (DOB/Country) to assign Risk Confidence.
    """
    hits = []
    logger.info("SCREENING: Engine active. Processing cross-reference table...")

    for cust in tqdm(customers, desc="Analysing Portfolios", unit="cust"):
        cust_name = cust.get('PrimaryLegalName', '')
        if not cust_name: continue

        cust_country = cust.get('ResidencyCountry', '')
        cust_dob = cust.get('DateOfBirth', '')

        for entity in sanctions_list:
            # 1. Name Analysis (Primary and Aliases)
            primary_name = entity.get('name', '')
            aliases_raw = entity.get('aliases', '') or ''
            aliases = [a.strip() for a in aliases_raw.replace(';', ',').split(',') if a.strip()]
            all_target_names = [primary_name] + aliases

            best_name_score = 0
            best_name_hit = ""

            for s_name in all_target_names:
                if not s_name: continue

                # Performance Pruning
                if abs(len(cust_name) - len(s_name)) > NAME_LENGTH_TOLERANCE:
                    continue

                score = calculate_weighted_score(cust_name, s_name)
                if score > best_name_score:
                    best_name_score = score
                    best_name_hit = s_name

            # 2. Decision Logic
            if best_name_score >= BASE_MATCH_THRESHOLD:
                s_countries = (entity.get('countries', '') or '').lower()
                s_dobs = (entity.get('birth_date', '') or '')

                # Secondary Attribute Validation
                country_match = cust_country.lower() in s_countries if cust_country else False
                dob_match = cust_dob[:4] in s_dobs if (cust_dob and s_dobs) else False

                # Confidence Classification
                confidence = "High" if (country_match or dob_match) else "Medium"
                if best_name_score >= CRITICAL_MATCH_THRESHOLD and (country_match or dob_match):
                    confidence = "CRITICAL"

                # 3. ALERT OBJECT GENERATION
                # TO ADD NEW FIELDS TO THE REPORT:
                # Add extra key-value pairs here (e.g., 'Passport': cust.get('ID_Number'))
                hits.append({
                    'Confidence': confidence,
                    'Score': round(best_name_score, 2),
                    'CustomerID': cust.get('CustomerID'),
                    'CustomerName': cust_name,
                    'CustomerDOB': cust_dob,
                    'CustomerCountry': cust_country,
                    'MatchedName': best_name_hit,
                    'MatchReason': f"Name ({round(best_name_score, 1)}%)" + (" + Country" if country_match else "") + (
                        " + DOB" if dob_match else ""),
                    'SanctionsID': entity.get('id'),
                    'Schema': entity.get('schema', 'UNKNOWN'),
                    'Dataset': entity.get('dataset', 'OPEN_SANCTIONS')
                })

    logger.info(f"SCREENING COMPLETE: Identified {len(hits)} potential matches for manual review.")
    return hits


def save_hits_to_csv(hits, output_file):
    """
    Exports alerts to a structured CSV for audit trail and case management systems.
    """
    if not hits:
        logger.info("REPORT: No alerts generated. Portfolio clean.")
        return

    logger.info(f"REPORT: Writing {len(hits)} alerts to {output_file}...")
    try:
        keys = hits[0].keys()
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(hits)
        logger.info("REPORT SUCCESS: CSV file is ready for compliance review.")
    except Exception as e:
        logger.error(f"REPORT ERROR: Failed to write output file. Details: {e}")


if __name__ == "__main__":
    logger.info("================================================================")
    logger.info("SYSTEM START: COMPLIANCE SCREENING ENGINE")
    logger.info("================================================================")

    # Data Acquisition
    sanctions_data = load_csv_data(SANCTIONS_FILE, "Sanctions Master List")
    customer_data = load_csv_data(CUSTOMER_FILE, "Internal Customer Portfolio")

    if sanctions_data and customer_data:
        # Sampling logic for efficiency testing
        test_sample = customer_data[:SCREEN_LIMIT] if SCREEN_LIMIT else customer_data

        match_results = screen_customers(test_sample, sanctions_data)

        if match_results:
            save_hits_to_csv(match_results, OUTPUT_FILE)

            # --- FORMATTED CONSOLE REPORTING ---
            print("\n" + "=" * 95)
            print(f"{'CONFIDENCE':<12} | {'SCORE':<6} | {'CUSTOMER NAME':<25} | {'MATCHED ENTITY':<25} | {'REASON'}")
            print("-" * 95)

            rank_map = {"CRITICAL": 0, "High": 1, "Medium": 2}
            sorted_hits = sorted(match_results, key=lambda x: (rank_map.get(x['Confidence'], 3), -x['Score']))

            for hit in sorted_hits[:20]:
                print(
                    f"{hit['Confidence']:<12} | {hit['Score']:<6} | {hit['CustomerName'][:25]:<25} | {hit['MatchedName'][:25]:<25} | {hit['MatchReason']}")

            print("=" * 95)
            print(f"REPORT SUMMARY: {len(match_results)} matches found. Full report saved to {OUTPUT_FILE}.")
        else:
            logger.info("FINAL RESULT: No suspicious matches identified above threshold.")
    else:
        logger.error("SYSTEM ABORT: Required data files are missing or corrupted.")

    logger.info("================================================================")
    logger.info("SYSTEM END: SCREENING CYCLE COMPLETE")
    logger.info("================================================================")