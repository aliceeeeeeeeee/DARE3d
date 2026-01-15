<div align="center">

# DARE3D: Division Axis Recognition in 3D

<a href="https://pytorch.org/get-started/locally/"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white"></a> <a href="https://pytorchlightning.ai/"><img alt="Lightning" src="https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white"></a> <a href="https://hydra.cc/"><img alt="Config: Hydra" src="https://img.shields.io/badge/Config-Hydra-89b8cd"></a> <a href="https://github.com/ashleve/lightning-hydra-template"><img alt="Template" src="https://img.shields.io/badge/-Lightning--Hydra--Template-017F2F?style=flat&logo=github&labelColor=gray"></a>

</div>

---

## Overview

**DARE3D** is a deep learning framework for detecting cell divisions in 3D biological image volumes and estimating their key attributes. This Python implementation leverages PyTorch Lightning and Hydra for configuration management to provide a flexible, reproducible pipeline for:

1. **Segmentation**: Detect the center (barycenter) of cell divisions
2. **Regression**: Estimate division attributes such as:
   - Orientation angle
   - Division axis length
   - Other morphological parameters

The framework supports both **training from custom datasets** and **inference on new data** using pre-trained models.

---

## Quick Start (Demo Mode)

The easiest way to get started is with the **included demo dataset** and pre-trained weights (downloaded automatically from Zenodo on first run):

```bash
# 1. Clone the repository
git clone https://github.com/JFRupprecht-OM/DARE3d
cd DARE3d

# 2. Create and activate conda environment
conda create -n dare3d python=3.10
conda activate dare3d

# 3. Install PyTorch (adapt CUDA version if needed)
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4. Install DARE3D and dependencies
pip install -r requirements.txt
pip install -e .

# 5. Run the prediction notebook
# Open and run: Run_dare3d_Prediction.ipynb
```

> **Note**: The demo dataset and pre-trained models (segmentation & regression) will be automatically downloaded on first use. No manual setup needed!

---

## Installation

### Prerequisites
- Python 3.10
- CUDA 11.8+ (for GPU training) or CPU-only mode
- Conda (recommended)

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/JFRupprecht-OM/DARE3d
cd DARE3d

# 2. Initialize your shell for conda (optional but recommended)
conda init powershell  # Windows PowerShell
# OR
conda init bash        # Linux/macOS

# 3. Create a fresh conda environment
conda create -n dare3d python=3.10
conda activate dare3d
```

#### Install PyTorch First (Critical!)

PyTorch wheels are CUDA-version specific. Install the correct variant **before** other dependencies:

```bash
# CUDA 12.1 (latest, recommended)
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# OR for CUDA 11.8
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# OR for CPU-only
python -m pip install torch torchvision torchaudio
```

#### Install DARE3D and Requirements

```bash
# Install remaining dependencies
pip install -r requirements.txt

# Install DARE3D in development mode
pip install -e .
```

### Special Configuration: Qt/napari (Optional)

If you encounter issues with `napari` GUI (specifically Qt):

```bash
# Install PyQt via conda-forge (recommended)
conda install -c conda-forge pyqt

# OR use an isolated napari environment
conda create -n napari-env python=3.10
conda activate napari-env
conda install -c conda-forge napari pyqt
```

### Enable Full Hydra Error Messages (PowerShell)

For better debugging, enable full Hydra stack traces:

```powershell
# For current session only:
$Env:HYDRA_FULL_ERROR = "1"

# To persist across sessions, add to your PowerShell profile:
notepad $PROFILE
# Add the line: $Env:HYDRA_FULL_ERROR = "1"
# Save and restart PowerShell
```

For Linux/macOS:
```bash
HYDRA_FULL_ERROR=1 python -m dare3d.train_eval
```

---

## Project Structure

```
dare3d/                          # Main package
├── data/                        # Data loading and preprocessing
│   ├── dare_datamodule.py      # PyTorch Lightning DataModule
│   ├── augmend_wrapper.py      # GPU-accelerated augmentations
│   ├── gpu_augmentations.py
│   ├── augmentations/          # Augmentation pipeline definitions
│   ├── components/             # Data pipeline components
│   └── visualization/          # Data visualization utilities
│
├── models/                      # Neural network architectures
│   ├── regression_module.py    # Regression model (attributes)
│   ├── segmentation_module.py  # Segmentation model (centers)
│   ├── tap_module.py           # Multi-task model variant
│   ├── sequence_ordered_module.py
│   ├── components/             # Model subcomponents
│   └── net/                    # Network backbone definitions
│
├── losses/                      # Custom loss functions
│   ├── angle3d.py              # 3D angle prediction loss
│   ├── decorrelation.py        # Decorrelation loss
│   └── pixelwise_crossentropy.py
│
├── metrics/                     # Evaluation metrics
│   ├── inference.py            # Inference pipeline
│   ├── infer_measure.py        # Measurement utilities
│   ├── object_level.py         # Object-level metrics
│   └── (others)
│
├── loggers/                     # Custom logging utilities
│   ├── segmentation_logger.py
│   └── regression_logger.py
│
├── tools/                       # Utility scripts and tools
├── utils/                       # Helper functions and utilities
│
├── train.py                     # Main training script (Hydra-based)
├── train_eval.py               # Combined training & evaluation
├── eval.py                      # Evaluation-only script
├── predict.py                   # Inference script
├── demo.py                      # Demo data download utility
└── __init__.py

configs/                         # Hydra configuration files
├── train.yaml                  # Training config template
├── eval.yaml                   # Evaluation config
├── predict.yaml                # Inference config
├── data/                       # Data config (segmentation, regression, etc.)
├── model/                      # Model architectures config
│   ├── criterion/              # Loss functions config
│   ├── metric/                 # Metrics config
│   ├── net/                    # Network config
│   ├── optimizer/              # Optimizer config
│   └── scheduler/              # LR scheduler config
├── trainer/                    # Trainer config (CPU, GPU, DDP, etc.)
├── logger/                     # Logger config (MLflow, TensorBoard, etc.)
├── callbacks/                  # PyTorch Lightning callbacks
├── debug/                      # Debug modes
├── experiment/                 # Experiment presets
└── hparams_search/             # Hyperparameter search configs

scripts/                        # Experiment generation scripts
├── generate_exp1.py           # Generate train/val/test splits
├── generate_exp2-7.py         # Other experiment variants
└── generation_utils.py

notebooks/                      # Jupyter notebooks
├── Run_dare3d_Prediction.ipynb # Main prediction notebook (START HERE!)
├── data_visualization.ipynb    # Interactive data exploration
└── data_normalization.ipynb    # Data preprocessing

tests/                          # Unit and integration tests
├── test_train.py
├── test_eval.py
├── test_configs.py
├── test_datamodules.py
└── helpers/

data/                           # Data storage (you'll populate this)
└── 3D/                         # Your 3D image data goes here

logs/                           # Training outputs (auto-generated)
├── segmentation_{dataset_name}/
│   └── runs/{date}/
│       ├── checkpoints/        # Model weights
│       ├── .hydra/             # Training config
│       └── (tensorboard logs)
└── regression_{dataset_name}/
    └── runs/{date}/
        ├── checkpoints/
        ├── .hydra/
        └── (tensorboard logs)

requirements.txt               # Python dependencies
setup.py                       # Package setup configuration
pyproject.toml                 # Project metadata & pytest config
Makefile                       # Development commands
README.md                      # This file
README.md.backup               # Original README (for reference)
```

---

## Configuration with Hydra

DARE3D uses **Hydra** for configuration management. This enables:

- **Composable configs**: Override settings via CLI without editing files
- **Experiment tracking**: Configs are automatically saved with each run
- **Multi-run capabilities**: Launch parameter sweeps with a single command

### Common Configuration Overrides

```bash
# Change device
python dare3d/train.py trainer=gpu          # GPU training
python dare3d/train.py trainer=cpu          # CPU training

# Change model
python dare3d/train.py model=segmentation   # Segmentation only
python dare3d/train.py model=regression     # Regression only

# Override specific parameters
python dare3d/train.py data.batch_size=8 model.lr=0.001

# Use an experiment preset
python dare3d/train.py experiment=segmentation
```

See [configs/](configs/) for all available configuration options.

---

## Training Models

### Quick Training (Demo Mode)

Use the included demo dataset for a quick validation run:

```bash
python dare3d/train_eval.py
```

### Train on Custom Dataset

#### 1. **Prepare Your Data**

Required folder structure:
```
your_dataset/
├── train/
│   ├── im/
│   │   ├── movie1.tif
│   │   └── movie2.tif
│   ├── label/
│   │   ├── movie1.tif
│   │   └── movie2.tif
│   └── sparse/          (optional - per-voxel weighting)
│       └── movie1.tif
├── val/
│   ├── im/
│   ├── label/
│   └── sparse/
└── test/
    ├── im/
    ├── label/
    └── sparse/
```

**Label Format**: Binary labeling of daughter cell pairs
- First daughter cell → odd values (1, 3, 5, ...)
- Second daughter cell → even values (2, 4, 6, ...)
- Connected component analysis extracts center pairs

**Sparse Weighting** (optional): 2D mask per frame indicating which voxels to use. Defaults to all-ones if omitted.

#### 2. **Register Your Data Scales**

Edit [data/3D/scales.json](data/3D/scales.json):
```json
{
  "movie1": [1.0, 1.0, 1.0],
  "movie2": [0.5, 0.5, 2.8]
}
```
Scales should be in **µm/voxel** for X, Y, Z respectively.

#### 3. **Train the Model**

```bash
# Train both segmentation and regression
python dare3d/train_eval.py --set_folder path/to/your_dataset --epoch 50

# Train segmentation only
python dare3d/train_eval.py --set_folder path/to/your_dataset --epoch 50 --train_segmentation True

# Train regression only
python dare3d/train_eval.py --set_folder path/to/your_dataset --epoch 50 --train_regression True

# Additional parameters (see train_eval.py for all)
python dare3d/train_eval.py \
  --set_folder path/to/your_dataset \
  --epoch 50 \
  --date 2025-05-01 \
  --batch_size 4 \
  --cell_radius 15
```

#### 4. **Monitor Training**

Checkpoints and logs are saved to:
```
logs/
├── segmentation_{dataset_name}/runs/{date}/
│   ├── checkpoints/
│   │   ├── epoch_10.ckpt
│   │   ├── epoch_best.ckpt
│   │   └── last.ckpt
│   └── .hydra/config.yaml       # Configuration used
└── regression_{dataset_name}/runs/{date}/
    └── checkpoints/
```

View tensorboard logs:
```bash
tensorboard --logdir logs/
```

---

## Inference (Prediction)

### Quickest Path: Use the Notebook

The easiest way to run inference is the **Jupyter notebook**:

```bash
jupyter notebook Run_dare3d_Prediction.ipynb
```

This notebook:
- Guides you through path setup
- Downloads demo data automatically (if needed)
- Runs both segmentation and regression
- Produces visualization outputs
- Supports comparison with ground truth

### Command-Line Inference

For programmatic or batch processing:

```bash
python dare3d/predict.py
```

Configuration is in [configs/predict.yaml](configs/predict.yaml). Key parameters:

```bash
python dare3d/predict.py \
  +model_dir=logs/segmentation_myDataset/runs/2025-05-01 \
  +data.test_data.data_dir=/path/to/input/movies \
  +output_dir=/path/to/output
```

#### Model Checkpoint Selection

The script automatically loads `.hydra/config.yaml` from the model directory. Specify which checkpoint:

```bash
python dare3d/predict.py \
  +model_dir=logs/segmentation_myDataset/runs/2025-05-01 \
  +ckpt_dir=checkpoints/epoch_best.ckpt
```

#### Scale Configuration

Movies must be registered with their correct pixel scales (in µm/voxel):

**Option 1 - JSON file (preferred)**:
```json
{
  "movie1.tif": [1.0, 1.0, 1.0],
  "movie2.tif": [0.5, 0.5, 2.8]
}
```
```bash
python dare3d/predict.py +scale_file=data/3D/scales.json
```

**Option 2 - Default scale** (same for all movies):
```bash
python dare3d/predict.py +default_scale=1.0
# OR for anisotropic voxels
python dare3d/predict.py +default_scale=[1.0, 1.0, 2.8]
```

**Option 3 - Target scale** (for network that was trained on specific scale):
```bash
python dare3d/predict.py +default_scale=1.0 +target_scale=1.0
```

---

## Testing

Run the test suite to verify your installation:

```bash
# Quick tests (excludes slow tests)
make test

# All tests (including slow ones)
make test-full

# Or using pytest directly
pytest -k "not slow"
pytest
```

Expected test categories:
- `test_configs.py` - Configuration loading
- `test_datamodules.py` - Data pipeline
- `test_train.py` - Training mechanics
- `test_eval.py` - Evaluation pipeline

---

## Data Preparation & Experiments

### Generate Experiment Splits

Use the provided scripts to organize your raw data:

```bash
# 1. Split movies along X axis (recommended preprocessing)
python scripts/generate_split_movies.py --data_dir data/3D

# 2. Generate experiment-specific train/val/test splits
python scripts/generate_exp1.py --data_dir data/3D
# exp2, exp3, ... exp7 also available
```

### Generate Sparse Weight Masks

To exclude specific regions from training (e.g., damaged areas):

```bash
python dare3d/tools/generate_sparse_weights.py \
  --annotated_label path/to/label.tif
```

---

## Development & Utilities

### Useful Make Commands

```bash
make help              # Show all available commands
make test              # Run quick tests
make test-full         # Run all tests
make format            # Run pre-commit hooks (code formatting)
make clean             # Remove build artifacts and caches
make clean-logs        # Remove all training logs
make sync              # Sync with upstream main branch
```

### Useful Utilities

**Visualize data**:
```bash
jupyter notebook notebooks/data_visualization.ipynb
```

**Normalize data**:
```bash
jupyter notebook notebooks/data_normalization.ipynb
```

**Check imports and dependencies**:
```bash
pip check                        # Verify environment consistency
python -c "from dare3d import *; print('Package imports OK')"
```

---

## License & Attribution

This repository is part of PhD research in 3D cell division analysis.

**Authors**: Romain Karpinski, Marc Karnat, Alice Gros, Qazi Saaheelur Rahaman, Jules Vanaret, Mehdi Saadaoui, Sham Tlili, and Jean-Francois Rupprecht

**Based on**: [Lightning-Hydra-Template](https://github.com/ashleve/lightning-hydra-template)

---

## Troubleshooting

### Issue: CUDA Out of Memory
- Reduce batch size: `--batch_size 2`
- Use CPU training: `trainer=cpu`
- Use gradient accumulation: `trainer.accumulate_grad_batches=2`

### Issue: napari/Qt GUI not working
```bash
conda install -c conda-forge pyqt
```

### Issue: Import errors after installation
```bash
pip install -e .  # Reinstall in editable mode
```

### Issue: Hydra config errors
```powershell
$Env:HYDRA_FULL_ERROR = "1"  # PowerShell - show full traceback
```

### Demo data not downloading
The demo folder downloads automatically from Zenodo on first run. If this fails:
- Check internet connection
- Verify Zenodo is accessible
- Manual download: [DARE3d_data.zip](https://zenodo.org/api/records/17456474/draft/files/DARE3d_data.zip)

---

## Additional Resources

- **Hydra Documentation**: https://hydra.cc/
- **PyTorch Lightning**: https://www.pytorchlightning.ai/
- **MONAI**: https://monai.io/ (medical imaging toolkit)

---

**Questions?** Check the demo notebook or open an issue on the repository.
