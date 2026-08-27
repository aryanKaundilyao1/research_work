import os

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WESAD_ROOT = os.path.join(PROJECT_ROOT, "datasets", "WESAD", "WESAD")
DATASET_B_ROOT = os.path.join(PROJECT_ROOT, "datasets", "Dataset_B", "wearable-device-dataset-from-induced-stress-and-structured-exercise-sessions-1.0.1")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Windowing Parameters
WINDOW_SIZE = 60
STEP_SIZE = 30

# Feature Extraction Modalities
# Note: HR and IBI are excluded by strict cross-dataset requirement
MODALITIES = ['EDA', 'TEMP', 'BVP', 'ACC']

# Machine Learning Parameters
RANDOM_SEED = 42
K_BEST = 20

# XGBoost Parameters
XGB_MAX_DEPTH = 3
XGB_N_ESTIMATORS = 50
XGB_REG_ALPHA = 1.0
XGB_LEARNING_RATE = 0.05
XGB_SUBSAMPLE = 0.8

# Dataset B Constraints
DATASET_B_EXCLUDE = ['f07']  # Excluded due to broken BVP/TEMP sensors
