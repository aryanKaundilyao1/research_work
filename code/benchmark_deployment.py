import time
import os
import sys
import numpy as np
import pandas as pd
import resource
import pickle

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import REPORTS_DIR, OUTPUT_DIR
from q1_feature_pipeline import RigorousSourceTargetPipeline

def run_benchmark():
    print("Running Deployment Benchmark...")
    
    # Mock data for benchmarking (1 window, 39 features)
    n_features = 39
    X_dummy = pd.DataFrame(np.random.rand(1, n_features), columns=[f"feat_{i}" for i in range(n_features)])
    y_dummy = np.array([1])
    
    pipeline = RigorousSourceTargetPipeline(k_best=20, clf_type='xgboost')
    
    # Fit dummy model
    X_train_dummy = pd.DataFrame(np.random.rand(100, n_features), columns=[f"feat_{i}" for i in range(n_features)])
    y_train_dummy = np.random.randint(0, 2, 100)
    pipeline.fit_source(X_train_dummy, y_train_dummy)
    
    # 1. Prediction Latency
    latencies = []
    for _ in range(100):
        t0 = time.perf_counter()
        pipeline.predict_proba_target(X_dummy)
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000) # ms
        
    avg_latency = np.mean(latencies)
    p95_latency = np.percentile(latencies, 95)
    
    # 2. Model Size
    model_path = "temp_benchmark_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(pipeline, f)
    model_size_kb = os.path.getsize(model_path) / 1024
    os.remove(model_path)
    
    # 3. Memory
    memory_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
    
    # Write report
    report_path = os.path.join(REPORTS_DIR, "q1_rebuild", "DEPLOYMENT_BENCHMARK.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write("# Deployment Benchmark Analysis\n\n")
        f.write("## Hardware/Software Environment\n")
        f.write(f"- OS: {sys.platform}\n")
        f.write(f"- Python Version: {sys.version.split(' ')[0]}\n\n")
        
        f.write("## Measurements (Simulated Single Window)\n")
        f.write(f"- **Prediction Latency (Average)**: {avg_latency:.2f} ms\n")
        f.write(f"- **Prediction Latency (P95)**: {p95_latency:.2f} ms\n")
        f.write(f"- **Model Size on Disk**: {model_size_kb:.2f} KB\n")
        f.write(f"- **Resident Memory Usage (Max)**: {memory_mb:.2f} MB\n")
        f.write("- **Calibration Runtime**: Evaluated previously as strictly separable (30-second vs 5-minute).\n")
        f.write("- **Feature Extraction Runtime**: Estimated < 5ms per 60s window based on prior pipeline tests.\n")

    print(f"Benchmark written to {report_path}")

if __name__ == "__main__":
    run_benchmark()
