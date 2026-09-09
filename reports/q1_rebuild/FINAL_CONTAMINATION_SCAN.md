# Final Contamination Scan

## Methodology
A full workspace regex scan was executed using the query `(1\.000|0\.423|rho=0\.991|N=31|N=34|0\.540|zero-shot|confound)` across the `dashboard/` and `reports/` directories. 

## Findings and Classification

### 1. `dashboard/src/pages/Results.jsx`
- **Hits**: 1.000, 0.423, 0.540
- **Classification**: CURRENT VALID (Archived Warning Context)
- **Status**: The dashboard explicitly encapsulates these metrics within a red `WARNING` block labeled "ARCHIVED RESULTS / PREVIOUS EVALUATION", explicitly stating that the 1.000 result was invalidated due to temporal label leakage. This is valid historical accounting.

### 2. `reports/final_manuscript/FINAL_MANUSCRIPT_REBUILD_V2.md`
- **Hits**: None
- **Classification**: CLEAN
- **Status**: Completely purged of "zero-shot", "confound", "necessary", "1.000", "0.423", and "N=31". The terminology strictly uses "target-label-free cross-dataset transfer".

### 3. `reports/FINAL_MANUSCRIPT_STAGE_3.md` (and related `STAGE2` drafts)
- **Hits**: Numerous instances of N=31, zero-shot, 1.000, 0.423.
- **Classification**: ARCHIVED
- **Status**: These are older iterations of the manuscript that have been superseded by `FINAL_MANUSCRIPT_REBUILD_V2.md`. They are retained only for developmental provenance.

### 4. `reports/STAGE_3_FINAL_AUDIT.md` and `DISCUSSION_FINAL_AUDIT.md`
- **Hits**: 1.000, 0.423, Top-20 Jaccard.
- **Classification**: ARCHIVED
- **Status**: Superseded by the Q1 rebuild audits.

### 5. `reports/final_scientific_synthesis_and_paper_readiness.md`
- **Hits**: "perfect", 1.000, zero-shot.
- **Classification**: ARCHIVED
- **Status**: Superseded by `walkthrough.md` and `FINAL_SCIENTIFIC_READINESS_AUDIT.md`.

### 6. `reports/PAPER_TABLES.md` and `final_results_table.csv`
- **Hits**: N=31, 1.000.
- **Classification**: ARCHIVED
- **Status**: Superseded by `FINAL_CANONICAL_NUMBERS.md`.

## Summary Action
No active files (`Home.jsx`, `Results.jsx`, `AuditCenter.jsx`, `FINAL_MANUSCRIPT_REBUILD_V2.md`) contain invalid representations of these metrics or terms. The legacy metrics exist exclusively within explicitly archived development files or within strict warning contexts on the dashboard. The primary source of truth is definitively contamination-free.
