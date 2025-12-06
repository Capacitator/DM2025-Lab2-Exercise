"""Complete automated pipeline: download (if needed), preprocess, train, and submit.

This script will:
1. Check for data files (download if possible)
2. Preprocess HDF5 files to .npz
3. Train models
4. Generate predictions
5. Create submission CSV

Run with: python run_complete_pipeline.py
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

# Try to download first
print("="*70)
print("BRAIN-TO-TEXT COMPLETE PIPELINE")
print("="*70)

# Step 0: Download data
print("\n[STEP 0] Checking for data files...")
download_script = BASE_DIR / "download_data.py"
if download_script.exists():
    result = subprocess.run([sys.executable, str(download_script)], cwd=BASE_DIR)
    if result.returncode != 0:
        print("\n⚠ Data download failed or files not found.")
        print("Please ensure data files are in:", DATA_DIR)
        print("Required: data_train.hdf5, data_val.hdf5, data_test.hdf5")
        
        # Check if files exist anyway
        all_exist = all((DATA_DIR / f"data_{split}.hdf5").exists() 
                       for split in ["train", "val", "test"])
        if not all_exist:
            print("\n❌ Cannot proceed without data files.")
            print("\nTo download manually:")
            print("1. Go to: https://www.kaggle.com/competitions/brain-to-text-25/data")
            print("2. Accept competition rules")
            print("3. Download the HDF5 files")
            print(f"4. Place them in: {DATA_DIR}")
            sys.exit(1)
        else:
            print("✓ Found data files, proceeding...")
else:
    # Check if files exist
    all_exist = all((DATA_DIR / f"data_{split}.hdf5").exists() 
                   for split in ["train", "val", "test"])
    if not all_exist:
        print("❌ Data files not found. Please download them first.")
        sys.exit(1)

# Step 1: Run full pipeline
print("\n[STEP 1] Running preprocessing, training, and inference...")
pipeline_script = BASE_DIR / "run_full_pipeline.py"
if pipeline_script.exists():
    result = subprocess.run([sys.executable, str(pipeline_script)], cwd=BASE_DIR)
    sys.exit(result.returncode)
else:
    print("❌ Pipeline script not found!")
    sys.exit(1)

