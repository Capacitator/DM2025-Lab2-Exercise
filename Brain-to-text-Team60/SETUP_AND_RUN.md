# Complete Setup and Run Guide

## Quick Start

Once you have the data files, run:

```bash
python run_complete_pipeline.py
```

This will automatically:
1. Check for data files
2. Preprocess HDF5 → .npz
3. Train the model
4. Generate submission CSV

## Data Download

### Option 1: Kaggle (Recommended)
1. Go to: https://www.kaggle.com/competitions/brain-to-text-25
2. Click "Join Competition" and accept the rules
3. Go to the "Data" tab
4. Download:
   - `data_train.hdf5`
   - `data_val.hdf5`
   - `data_test.hdf5`
5. Place all files in: `Brain-to-text-Team60/data/`

### Option 2: Automated Download
```bash
python download_data.py
```
(Note: May be rate-limited. If so, use Option 1)

### Option 3: Dryad Repository
1. Go to: https://datadryad.org/dataset/doi:10.5061/dryad.dncjsxm85
2. Download the dataset
3. Extract and place HDF5 files in `Brain-to-text-Team60/data/`

## Manual Pipeline Steps

If you prefer to run steps individually:

### 1. Preprocessing
```bash
python post_process_dataset/preprocess.py \
  --input data/data_train.hdf5 \
  --output data/processed/train_meanpool.npz \
  --method meanpool --window 20 --stride 20

python post_process_dataset/preprocess.py \
  --input data/data_val.hdf5 \
  --output data/processed/val_meanpool.npz \
  --method meanpool --window 20 --stride 20

python post_process_dataset/preprocess.py \
  --input data/data_test.hdf5 \
  --output data/processed/test_meanpool.npz \
  --method meanpool --window 20 --stride 20
```

### 2. Training
```bash
python model_of_decoding/train.py \
  --config model_of_decoding/configs/baseline_knn.yaml
```

### 3. Generate Submission
```bash
python model_of_decoding/predict.py \
  --model-path outputs/baseline_knn/models/nearest_neighbor.joblib \
  --feature-bundle data/processed/test_meanpool.npz \
  --output submissions/nearest_neighbor_meanpool.csv \
  --top-k 3
```

## Expected Outputs

After running the pipeline, you'll have:

- **Model**: `outputs/baseline_knn/models/nearest_neighbor.joblib`
- **Validation Metrics**: `outputs/baseline_knn/metrics/validation_metrics.json`
- **Submission CSV**: `submissions/nearest_neighbor_meanpool.csv`

## Upload to Kaggle

1. Go to: https://www.kaggle.com/competitions/brain-to-text-25/submit
2. Upload `submissions/nearest_neighbor_meanpool.csv`
3. Check your leaderboard score!

## Troubleshooting

### "Data files not found"
- Ensure all 3 HDF5 files are in `Brain-to-text-Team60/data/`
- Check file names are exactly: `data_train.hdf5`, `data_val.hdf5`, `data_test.hdf5`

### "Rate limited" when downloading
- Wait 5-10 minutes and try again
- Or download manually from Kaggle website

### "Module not found" errors
- Install dependencies: `pip install -r requirements.txt`

### Out of memory during preprocessing
- Process files one at a time
- Consider using a machine with more RAM
- The files are large (several GB each)

