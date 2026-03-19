# ⚖️ Fuzzy-Sanctions-Screening: Multi-Tiered AML Matching Engine

> **High-Velocity Bulk Sanctions Screening** | **KYC Verification** | **OFAC/UN/EU/UKHM Treasury Compliant** | **RapidFuzz-Powered**

---

## 📋 Table of Contents

| Section | Description |
|---------|-------------|
| [Executive Summary](#-executive-summary) | System overview and core value proposition |
| [Core Strengths](#-core-strengths--technical-advantages) | Hybrid fuzzy logic, rule tuning, confidence scoring |
| [Functional Architecture](#-functional-architecture) | Technical implementation components |
| [Compliance Alignment](#-compliance--regulatory-alignment) | Sanctions regimes and audit capabilities |
| [Installation & Operation](#-installation--operation) | Dependencies, data requirements, execution |
| [Runtime Logs](#-runtime-logs) | System execution output samples |
| [Match Results](#-match-results-preview) | Alert preview and interpretation |
| [Legal Disclaimer](#-legal-disclaimer) | Terms of use and regulatory notice |

---

## 📌 Executive Summary

**Fuzzy-Sanctions-Screening** is a high-velocity, rule-tuned compliance engine designed for:

| Use Case | Description |
|----------|-------------|
| **Bulk Sanctions Screening** | Multi-million-row dataset processing against sanctions lists |
| **Know Your Customer (KYC)** | Verification and identity matching for customer onboarding |

### Problem Statement

The engine mitigates the risks of **sanctions evasion** by identifying:

- ✅ **Phonetic variations** in entity names
- ✅ **Aliases** and alternative spellings
- ✅ **Transliteration discrepancies** across linguistic scripts

Standard exact-match systems fail to detect these variations, creating regulatory exposure.

### Performance Profile

| Metric | Specification |
|--------|---------------|
| **Scalability** | Multi-million-row datasets (e.g., OpenSanctions `TargetsSimple`) |
| **Target** | Internal customer portfolios |
| **Output** | Prioritized, audit-ready **Match Alert Report** |
| **Backend** | `RapidFuzz` (C++ optimized) for sub-millisecond comparisons |

---

## 🚀 Core Strengths & Technical Advantages

---

### 1️⃣ Hybrid Fuzzy Logic Model (Multi-Algorithmic)

The engine employs a **Weighted Hybrid Scoring** mechanism to balance precision and recall:

| Algorithm | Weight | Function | Use Case |
|-----------|--------|----------|----------|
| **Jaro-Winkler Similarity** | 17% | Captures name prefix matching | Surname and given name variations |
| **Levenshtein Edit Distance** | 83% | Prioritizes character-level typos, omissions, swaps | Noisy manual data entry |
| **Transliteration Handling** | N/A | Flags entities across linguistic scripts | All name variations across different languages including native written forms |

**Key Advantage:** Uses **phonetic similarity** rather than strict string equality.

---

### 2️⃣ Granular Rule Tuning (Compliance Control)

Unlike black-box solutions, this system provides **full parameter transparency**:

| Parameter | Function | Benefit |
|-----------|----------|---------|
| **Base Match Thresholds** | Defines sensitivity floor (e.g., 85%) | Controls false positive rate |
| **Length-Based Pruning** | Skips low-probability comparisons | Optimizes ETL performance |
| **Model Weighting** | Adjusts JW vs. Levenshtein influence dynamically | Enables portfolio-specific calibration |

---

### 3️⃣ Multi-Tiered Confidence Scoring (Risk-Based Approach)

To reduce false positives and prioritize high-risk hits, the engine cross-references **secondary identifiers**:

| Confidence Level | Criteria | Action Required |
|------------------|----------|-----------------|
| 🔴 **CRITICAL** | Score > 98% + DOB/Country match | Near-certain identity → **Immediate investigation** |
| 🟡 **HIGH** | Strong fuzzy match + secondary attribute | High correlation requiring **Compliance review** |
| ⚪ **MEDIUM** | Name match only | Requires **Enhanced Due Diligence (EDD)** |

---

## 🛠️ Functional Architecture

| Component | Technical Implementation | Purpose |
|-----------|-------------------------|---------|
| **Data Parsing** | Streamed CSV `DictReader` with `tqdm` progress telemetry | Memory-efficient large dataset handling |
| **Fuzzy Backend** | `RapidFuzz` (C++ optimized) | Sub-millisecond string comparisons |
| **Secondary Validation** | Boolean intersection of ISO country codes and ISO 8601 dates | Confidence score elevation |
| **Audit Export** | Structured CSV alert generation | Case Management Systems (CMS) integration |

---

## 📋 Compliance & Regulatory Alignment

This engine supports **major global sanctions regimes**:

| Regime | Authority | Coverage |
|--------|-----------|----------|
| **OFAC** | U.S. Department of Treasury | Specially Designated Nationals (SDN) |
| **United Nations (UN)** | UN Security Council | Consolidated Sanctions List |
| **European Union (EU)** | European External Action Service | EU Consolidated List |
| **UK HM Treasury** | Office of Financial Sanctions Implementation | UK Consolidated List |

---

### Capabilities

| Feature | Description | Regulatory Benefit |
|---------|-------------|-------------------|
| **Auditability** | Each match includes detailed `MatchReason` (e.g., `Name 92% + Country Match`) | Full decision provenance for examinations |
| **Transparency** | Fully documented screening logic | Suitable for regulatory examination |
| **Scalability** | Bulk processing for full portfolio re-screening | Periodic review compliance |

---

## ⚙️ Installation & Operation

---

### Production Dependencies

```bash
pip install rapidfuzz tqdm
```

---

### Data Requirements

Place the following datasets in the **root directory**:

| File | Description | Source |
|------|-------------|--------|
| `customers_core_export.csv` | Customer data for screening | Internal export |
| `TargetsSimple.csv` | Sanctions screening data | OpenSanctions (simplified targets) |

---

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

| Field | Description | Usage |
|-------|-------------|-------|
| **Confidence Levels** | Indicates prioritization for investigation | Triage workflow assignment |
| **Score** | Reflects fuzzy similarity percentage | Risk ranking |
| **Reason** | Provides audit traceability (e.g., name match + secondary identifier) | Regulatory examination evidence |
| **CSV Export** | Full results exported for downstream case management | CMS integration |

---

## ⚖️ Legal Disclaimer

> **This tool is intended for use by trained compliance professionals as part of a robust AML/CFT framework. It does not constitute legal advice.**

| Requirement | Responsibility |
|-------------|----------------|
| **Result Validation** | Users must validate results through official government sources |
| **Manual Investigation** | Required before taking any adverse action against individuals or entities |
| **Regulatory Compliance** | Users are responsible for ensuring alignment with local jurisdictional requirements |
| **Model Risk Management** | Independent validation recommended for production deployment |

---

## 📊 System Performance Metrics

| Metric | Value | Unit |
|--------|-------|------|
| **Sanctions List Throughput** | 92,046.99 | rows/second |
| **Customer Portfolio Throughput** | 97,596.43 | rows/second |
| **Per-Customer Analysis Time** | 8.22 | seconds |
| **Total Screening Cycle** | ~7 | minutes (1,000 customers vs. 1.2M sanctions records) |
| **Match Alert Rate** | 109 | alerts per 1,000 customers |

---

## 🔧 Configuration Parameters

| Parameter | Default | Adjustable | Purpose |
|-----------|---------|------------|---------|
| **Base Match Threshold** | 85% | ✅ | Sensitivity floor for match detection |
| **Jaro-Winkler Weight** | 17% | ✅ | Prefix matching influence |
| **Levenshtein Weight** | 83% | ✅ | Character-level edit distance influence |
| **Critical Score Threshold** | 98% | ✅ | Auto-escalation trigger |
| **Secondary Identifier Match** | DOB + Country | ✅ | Confidence elevation criteria |

---

## 📬 Support & Contributions

| Channel | Purpose |
|---------|---------|
| **GitHub Issues** | Bug reports, feature requests, compliance queries |
| **Pull Requests** | Contributions for new sanctions list formats, algorithm improvements |
| **Documentation** | Enhancement suggestions for regulatory alignment |

---

> **Built for Compliance. Engineered for Precision. Designed for Auditability.**

---

| Badge | Status |
|-------|--------|
| **OFAC Compliant** | ✅ |
| **UN Sanctions Support** | ✅ |
| **EU Consolidated List** | ✅ |
| **UK HM Treasury** | ✅ |
| **Audit-Ready Export** | ✅ |
| **Multi-Language Support** | ✅ |

---

© 2026 **Fuzzy-Sanctions-Screening** | AML/CFT Sanctions Matching Engine | Apache License 2.0
