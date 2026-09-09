import os
import sys

# We simply invoke run_final_audit.py, as it was strictly designed as the reproducibility runner 
# incorporating all correct paths and 30s calib / strict temporal separation tests.

def main():
    print("Executing final reproducibility pipeline...")
    os.system(f"{sys.executable} {os.path.join(os.path.dirname(__file__), 'run_final_audit.py')}")
    
if __name__ == '__main__':
    main()
