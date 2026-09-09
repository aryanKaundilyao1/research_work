# Deployment Benchmark Analysis

## Hardware/Software Environment
- OS: darwin
- Python Version: 3.13.9

## Measurements (Simulated Single Window)
- **Prediction Latency (Average)**: 0.67 ms
- **Prediction Latency (P95)**: 1.06 ms
- **Model Size on Disk**: 74.10 KB
- **Resident Memory Usage (Max)**: 201.31 MB
- **Calibration Runtime**: Evaluated previously as strictly separable (30-second vs 5-minute).
- **Feature Extraction Runtime**: Estimated < 5ms per 60s window based on prior pipeline tests.
