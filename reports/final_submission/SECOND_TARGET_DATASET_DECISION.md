# Second Target Dataset Decision

## Overview
During the final faculty audit, the addition of a second external target dataset (e.g., SWELL-KW) was evaluated.

## Decision: NOT INTEGRATED (SCIENTIFICALLY JUSTIFIED LIMITATION)

### Rationale
1. **Data Access & Privacy Constraints**: Reputable physiological stress datasets (such as SWELL-KW via DANS) require authenticated researcher credentialing and signed Data Use Agreements (DUAs) prohibiting automated mass-downloading or uncredentialed server access.
2. **Harmonization Risk**: The current pipeline is strictly calibrated to the Empatica E4 sensor on the WESAD and Hongn datasets, utilizing a massive 18.55 million rows and a 30-second target-label-free calibration buffer. Introducing an entirely new protocol (e.g., cognitive workload instead of physiological stressors) and entirely new sensors (e.g., Kinect, different ECG) at the absolute final stage introduces extreme methodological risk and potential for silent leakage.
3. **Scientific Completeness**: The current cross-dataset framework already satisfies the objective of evaluating target-label-free transfer across entirely disjoint cohorts. The performance drop and subsequent recovery via baseline calibration is robustly documented.

### Manuscript Action
This omission is explicitly stated in the manuscript's **10. Limitations** section:
> "The evidence is restricted by small sample sizes (N=15 source, N=35 target) and evaluation across a single source-target dataset pair. Replication across additional independent wearable cohorts (e.g., SWELL-KW, AffectiveROAD) remains a necessary step to establish broader generalizability, but requires careful harmonization of varying stressor protocols and sensor sampling rates."
