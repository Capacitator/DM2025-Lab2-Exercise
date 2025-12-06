"""Download brain-to-text competition data from Kaggle or Dryad."""

from __future__ import annotations

import os
import sys
import time
import zipfile
from pathlib import Path

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    KAGGLE_AVAILABLE = True
except ImportError:
    KAGGLE_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = [
    "data_train.hdf5",
    "data_val.hdf5", 
    "data_test.hdf5"
]


def download_from_kaggle() -> bool:
    """Download data using Kaggle API."""
    if not KAGGLE_AVAILABLE:
        print("Kaggle API not available. Install with: pip install kaggle")
        return False
    
    # Check for kaggle.json
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    if not kaggle_json.exists():
        print("Kaggle credentials not found.")
        print("Please download kaggle.json from https://www.kaggle.com/settings and place it in:")
        print(f"  {kaggle_dir}")
        return False
    
    try:
        api = KaggleApi()
        api.authenticate()
        print("Authenticated with Kaggle API")
        
        # Competition name from README
        competition = "brain-to-text-25"
        print(f"Downloading data from competition: {competition}")
        
        # Retry logic with exponential backoff
        max_retries = 5
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_time = min(2 ** attempt, 60)  # Exponential backoff, max 60s
                    print(f"Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                    time.sleep(wait_time)
                
                api.competition_download_files(competition, path=str(DATA_DIR))
                
                # Extract zip files if any
                for zip_file in DATA_DIR.glob("*.zip"):
                    print(f"Extracting {zip_file.name}...")
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(DATA_DIR)
                    zip_file.unlink()  # Remove zip after extraction
                
                # Check if files exist
                all_found = all((DATA_DIR / f).exists() for f in REQUIRED_FILES)
                if all_found:
                    print("✓ All data files downloaded successfully!")
                    return True
                else:
                    # List what we got
                    print("\nFiles in data directory:")
                    for f in sorted(DATA_DIR.glob("*")):
                        if f.is_file():
                            size_mb = f.stat().st_size / (1024 * 1024)
                            print(f"  {f.name}: {size_mb:.2f} MB")
                    print("\nSome required files are missing after download")
                    return False
                    
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    if attempt < max_retries - 1:
                        print(f"Rate limited. Retrying...")
                        continue
                    else:
                        print(f"Rate limited after {max_retries} attempts.")
                        print("Please wait a few minutes and try again, or download manually.")
                        return False
                else:
                    raise
        
        return False
            
    except Exception as e:
        print(f"Error downloading from Kaggle: {e}")
        return False


def download_from_dryad() -> bool:
    """Attempt to download from Dryad repository."""
    if not REQUESTS_AVAILABLE:
        print("Requests library not available. Install with: pip install requests")
        return False
    
    print("Attempting to download from Dryad repository...")
    print("Note: Dryad may require manual download from:")
    print("  https://datadryad.org/dataset/doi:10.5061/dryad.dncjsxm85")
    
    # Dryad doesn't provide direct download links easily
    # User would need to download manually
    return False


def check_existing_files() -> bool:
    """Check if data files already exist."""
    existing = [f for f in REQUIRED_FILES if (DATA_DIR / f).exists()]
    if len(existing) == len(REQUIRED_FILES):
        print("✓ All data files already exist!")
        for f in REQUIRED_FILES:
            size_mb = (DATA_DIR / f).stat().st_size / (1024 * 1024)
            print(f"  {f}: {size_mb:.2f} MB")
        return True
    elif existing:
        print(f"Found {len(existing)}/{len(REQUIRED_FILES)} files:")
        for f in existing:
            size_mb = (DATA_DIR / f).stat().st_size / (1024 * 1024)
            print(f"  ✓ {f}: {size_mb:.2f} MB")
        missing = [f for f in REQUIRED_FILES if f not in existing]
        print(f"Missing: {', '.join(missing)}")
    return False


def main():
    """Main download function."""
    print("="*60)
    print("Brain-to-Text Data Download")
    print("="*60)
    
    # Check if files already exist
    if check_existing_files():
        return 0
    
    print(f"\nData directory: {DATA_DIR}")
    print(f"Required files: {', '.join(REQUIRED_FILES)}")
    
    # Try Kaggle first
    print("\n[Method 1] Trying Kaggle API...")
    if download_from_kaggle():
        return 0
    
    # Try Dryad
    print("\n[Method 2] Trying Dryad...")
    if download_from_dryad():
        return 0
    
    # Manual instructions
    print("\n" + "="*60)
    print("MANUAL DOWNLOAD REQUIRED")
    print("="*60)
    print("\nPlease download the data files manually:")
    print("\n1. Kaggle Competition:")
    print("   https://www.kaggle.com/competitions/brain-to-text-25/data")
    print("   - Accept competition rules")
    print("   - Download data_train.hdf5, data_val.hdf5, data_test.hdf5")
    print("\n2. Or from Dryad:")
    print("   https://datadryad.org/dataset/doi:10.5061/dryad.dncjsxm85")
    print("\n3. Place the files in:")
    print(f"   {DATA_DIR}")
    print("\nThen run this script again to verify.")
    
    return 1


if __name__ == "__main__":
    sys.exit(main())

