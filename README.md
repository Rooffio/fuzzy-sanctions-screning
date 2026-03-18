# ⚖️ Fuzzy-Sanctions-Screening: Multi-Tiered AML Matching Engine

## 📌 Executive Summary

**Fuzzy-Sanctions-Screening** is a high-velocity, rule-tuned compliance engine designed for **Bulk Sanctions Screening** and **Know Your Customer (KYC)** verification.

It mitigates the risks of sanctions evasion by identifying phonetic variations, aliases, and transliteration discrepancies that standard exact-match systems fail to detect.

Built for scalability, the engine processes multi-million-row datasets (e.g., OpenSanctions `TargetsSimple`) against internal customer portfolios, delivering a prioritized, audit-ready **Match Alert Report**.

---

## 🚀 Core Strengths & Technical Advantages

### 1. Hybrid Fuzzy Logic Model (Multi-Algorithmic)

The engine employs a **Weighted Hybrid Scoring** mechanism to balance precision and recall:

* **Jaro-Winkler Similarity (17% weight)**

  * Captures name prefix matching
  * Effective for surname and given name variations

* **Levenshtein Edit Distance (83% weight)**

  * Prioritizes character-level typos, omissions, and swaps
  * Handles noisy manual data entry

* **Transliteration Handling**

  * Flags entities across linguistic scripts
  * Can handle all name variations across different languages including in their written language
  * Uses phonetic similarity rather than strict string equality

---

### 2. Granular Rule Tuning (Compliance Control)

Unlike black-box solutions, this system provides **full parameter transparency**:

* **Base Match Thresholds**

  * Defines sensitivity floor (e.g., 85%)

* **Length-Based Pruning**

  * Skips low-probability comparisons
  * Optimizes ETL performance

* **Model Weighting**

  * Adjust JW vs. Levenshtein influence dynamically
  * Enables portfolio-specific calibration

---

### 3. Multi-Tiered Confidence Scoring (Risk-Based Approach)

To reduce false positives and prioritize high-risk hits, the engine cross-references secondary identifiers:

* 🔴 **CRITICAL**

  * Score > 98% + DOB/Country match
  * Near-certain identity → immediate investigation

* 🟡 **HIGH**

  * Strong fuzzy match + secondary attribute
  * High correlation requiring review

* ⚪ **MEDIUM**

  * Name match only
  * Requires Enhanced Due Diligence (EDD)

---

## 🛠 Functional Architecture

| Component            | Technical Implementation                                          |
| -------------------- | ----------------------------------------------------------------- |
| Data Parsing         | Streamed CSV `DictReader` with `tqdm` progress telemetry          |
| Fuzzy Backend        | `RapidFuzz` (C++ optimized) for sub-millisecond comparisons       |
| Secondary Validation | Boolean intersection of ISO country codes and ISO 8601 dates      |
| Audit Export         | Structured CSV alert generation for Case Management Systems (CMS) |

---

## 📋 Compliance & Regulatory Alignment

This engine supports major sanctions regimes:

* OFAC
* United Nations (UN)
* European Union (EU)
* UK HM Treasury

### Capabilities

* **Auditability**

  * Each match includes detailed `MatchReason`
  * Example: `Name 92% + Country Match`

* **Transparency**

  * Fully documented screening logic
  * Suitable for regulatory examination

* **Scalability**

  * Bulk processing for full portfolio re-screening

---

## ⚙️ Installation & Operation

### Production Dependencies

```bash
pip install rapidfuzz tqdm
```

### Data Requirements

Place the following datasets in the root directory:

- **Customer data for screening**  
  `customers_core_export.csv`

- **Sanctions screening data from OpenSanctions (simplified targets)**  
  `TargetsSimple.csv`


### Execution

```bash
python ScreeningEngineTargetSimple.py
```

---

## 🖥️ Runtime Logs

```text
17:17:51 - INFO - ================================================================
17:17:51 - INFO - SYSTEM START: COMPLIANCE SCREENING ENGINE
17:17:51 - INFO - ================================================================
17:17:51 - INFO - INIT: Loading Sanctions Master List...
Importing Sanctions Master List:  98%|█████████▊| 1246496/1271335 [00:13<00:00, 92046.99 rows/s]
17:18:06 - INFO - SUCCESS: 1246496 records imported.
17:18:06 - INFO - INIT: Loading Internal Customer Portfolio...
Importing Internal Customer Portfolio: 100%|██████████| 1000/1000 [00:00<00:00, 97596.43 rows/s]
17:18:06 - INFO - SUCCESS: 1000 records imported.
17:18:06 - INFO - SCREENING: Engine active. Processing cross-reference table...
Analysing Portfolios: 100%|██████████| 50/50 [06:50<00:00,  8.22s/cust]
17:24:57 - INFO - SCREENING COMPLETE: Identified 109 potential matches for manual review.
17:24:57 - INFO - REPORT: Writing 109 alerts to screening_alerts.csv...
17:24:57 - INFO - REPORT SUCCESS: CSV file is ready for compliance review.
17:24:57 - INFO - ================================================================
17:24:57 - INFO - SYSTEM END: SCREENING CYCLE COMPLETE
17:24:57 - INFO - ================================================================
```

---

## 📋 Match Results Preview

```text
===============================================================================================
CONFIDENCE   | SCORE  | CUSTOMER NAME             | MATCHED ENTITY            | REASON
-----------------------------------------------------------------------------------------------
High         | 85.05  | Christopher Wells         | Christopher Bellamy       | Name (85.1%) + DOB
Medium       | 100.0  | Timothy Davis             | TIMOTHY DAVIS             | Name (100.0%)
Medium       | 100.0  | Timothy Davis             | Timothy Davis             | Name (100.0%)
Medium       | 100.0  | Christopher Wells         | Christopher Wells         | Name (100.0%)
Medium       | 100.0  | Christopher Wells         | Christopher Wells         | Name (100.0%)
Medium       | 100.0  | Laura Hall                | Laura Hall                | Name (100.0%)
Medium       | 100.0  | 李东                        | 李东                        | Name (100.0%)
Medium       | 94.72  | Christopher Wells         | Christopher Ellis         | Name (94.7%)
Medium       | 94.04  | Stephanie Reid            | Stephanie L Reid          | Name (94.0%)
Medium       | 93.13  | James Chukwu              | James Chukwudi            | Name (93.1%)
Medium       | 93.09  | Timothy Davis             | Timothy Davie             | Name (93.1%)
Medium       | 92.56  | Christopher Wells         | Christopher L. Wells      | Name (92.6%)
Medium       | 92.31  | Christopher Wells         | Christopher Powell        | Name (92.3%)
Medium       | 91.84  | Christopher Wells         | Christopher Bell          | Name (91.8%)
Medium       | 91.73  | Mark Chukwu               | Mary Chukwu               | Name (91.7%)
Medium       | 91.02  | Laura Hall                | LAURA HILL                | Name (91.0%)
Medium       | 90.94  | Stephanie Reid            | STEPHANIE RIEDY           | Name (90.9%)
Medium       | 90.78  | Timothy Davis             | Timothy Davidson          | Name (90.8%)
Medium       | 90.3   | Christopher Wells         | Kristopher Wells          | Name (90.3%)
Medium       | 90.04  | Christopher Wells         | Christopher Worrell       | Name (90.0%)
===============================================================================================
REPORT SUMMARY: 109 matches found. Full report saved to screening_alerts.csv.
```

---

## 🧾 Interpretation Notes

* **Confidence Levels** indicate prioritization for investigation
* **Score** reflects fuzzy similarity percentage
* **Reason** provides audit traceability (e.g., name match + secondary identifier)
* Full results are exported to a CSV for downstream case management workflows

---
## ⚖️ Legal Disclaimer

This tool is intended for use by trained compliance professionals as part of a robust AML/CFT framework. It does **not** constitute legal advice.

Users must validate results through official government sources and manual investigation before taking any adverse action against individuals or entities.
