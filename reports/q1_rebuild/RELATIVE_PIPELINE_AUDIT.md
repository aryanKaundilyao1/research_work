# Relative Training Pipeline Audit

Verified that the baseline-relative classifier is correctly trained using a baseline-relative WESAD representation.
The exact processing sequence enforced is:

1. **SOURCE SUBJECT**: WESAD baseline -> subject stats -> normalize source -> windows -> features.
2. **SOURCE TRAINING**: SelectKBest -> StandardScaler -> SMOTE -> Classifier.
3. **TARGET SUBJECT**: Target calibration baseline -> target stats -> normalize target -> features.
4. **TARGET INFERENCE**: Frozen SelectKBest -> Frozen StandardScaler -> Frozen Classifier.

PASS: Absolute source features are NEVER used to test relative target features.
