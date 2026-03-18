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

## ⚖️ Legal Disclaimer

This tool is intended for use by trained compliance professionals as part of a robust AML/CFT framework. It does **not** constitute legal advice.

Users must validate results through official government sources and manual investigation before taking any adverse action against individuals or entities.
