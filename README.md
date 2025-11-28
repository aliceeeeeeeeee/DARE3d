<div align="center">

# dare3d on Pytorch

<a href="https://pytorch.org/get-started/locally/"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white"></a> <a href="https://pytorchlightning.ai/"><img alt="Lightning" src="https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white"></a> <a href="https://hydra.cc/"><img alt="Config: Hydra" src="https://img.shields.io/badge/Config-Hydra-89b8cd"></a> <a href="https://github.com/ashleve/lightning-hydra-template"><img alt="Template" src="https://img.shields.io/badge/-Lightning--Hydra--Template-017F2F?style=flat&logo=github&labelColor=gray"></a><br>

</div>

## Description

**D**ivision **A**xis **RE**cognition in **3D** tissues

This repository contains the Python implementation to detect cell divisions (positions) and their attributes (i.e. angle and length) for 3D images.

Our approach relies on two steps:

* Cell division detection using semantic segmentation to detect the center of the division
* Cell attribute regression on detected divisions

## Summary

* [Native installation](#installation)

## Installation

```bash
# clone project
git clone https://github.com/JFRupprecht-OM/DARE3d
cd DARE3d

#To distinguish between your base and virtual environment(dare3d) in your command prompt, run either of the below
conda init powershell
conda init bash

# create conda environment
conda create -n dare3d python=3.10
conda activate dare3d
```
> **Important:** PyTorch CUDA wheels must be installed *before* installing the rest of the Python requirements (they are platform- and CUDA-version-specific and are served from PyTorch's wheel index). The `requirements.txt` in this repo excludes `torch`, `torchvision` and `torchaudio` so that the correct CUDA wheel can be installed first.

```bash
# install PyTorch + CUDA wheels (example: CUDA 12.1)
# Change `cu121` to the appropriate CUDA build for your system if needed (e.g. cu118, cu126).
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# install the rest of requirements
pip install -r requirements.txt

# install project in editable mode
pip install -e .
```

If you prefer CPU-only installation (or if your system drivers don't match a CUDA wheel), you can instead install CPU wheels explicitly by adapting it in `requirements.txt` accordingly.

#### HYDRA_FULL_ERROR (PowerShell)

To enable full Hydra tracebacks in PowerShell for the current session, run:

```powershell
$Env:HYDRA_FULL_ERROR = "1"
```

To persist this in every new PowerShell session, add the same line to your PowerShell profile (e.g. `notepad $PROFILE` -> paste the line -> save).

You can also set the same variable for a single run on Linux/macOS when you are running a command, for example:

```bash
HYDRA_FULL_ERROR=1 python -m dare3d.train_eval
```

#### Napari / Qt note

`napari` is included in `requirements.txt`, but GUI toolkits (Qt) are often easier to install via conda. If you encounter issues launching napari after `pip install -r requirements.txt`, install a Qt backend via conda-forge:

```bash
conda install -c conda-forge pyqt
# or create an isolated environment
conda create -n napari-env python=3.10
conda activate napari-env
conda install -c conda-forge napari pyqt
```

This avoids many binary compatibility problems on different platforms.

## Project folder structure

The project folder structure is as follow:

```
- config    # Contains the hydra configuration files
- data      # This is where the data is locate
- dare3d   # This is the library package that defines the model, the dataset...
- scripts   # Contains the scripts to run the experiments
- logs      # Contains the logs of the experiments
- Run_dare3d_Prediction.ipynb - jupyter notebook which runs the prediction on videos
```

> Note on `data`: inside the `data` folder you should create the dataset splits used for training, validation and testing. A common layout is shown in the "Retraining dataset" section below (train/im, train/label, etc.). Follow that structure so the data loader and helper scripts can find the movies and their annotations.


## Training and Evaluating

This repository provides `train_eval.py` to train and evaluate models on your movies. The script supports training segmentation and regression models together or independently, and also evaluation-only mode. Below are example usages (bash style) — adapt paths and flags to your environment.

**Case 1 — Train both segmentation and regression, then evaluate**

```bash
python dare3d/train_eval.py --set_folder <folder_with_training_data> --epoch <num_epochs> --date <experiment_date>
```

**Case 2 — Train only segmentation and evaluate**

```bash
python dare3d/train_eval.py --set_folder <folder_with_training_data> --epoch <num_epochs> --date <experiment_date> --train_segmentation True --train_regression False
```

**Case 3 — Train only regression and evaluate**

```bash
python dare3d/train_eval.py --set_folder <folder_with_training_data> --epoch <num_epochs> --date <experiment_date> --train_segmentation False --train_regression True
```

**Case 4 — Evaluation only (use existing weights)**

```bash
python dare3d/train_eval.py --set_folder <folder_with_training_data> --epoch <num_epochs> --date <experiment_date> --eval_only True
```

You can pass additional parameters (for example `--batch_size`, `--cell_radius`, etc.) in the same way; inspect `train_eval.py` for full list of supported command-line arguments and their defaults. If you prefer PowerShell on Windows, the same commands work but replace line continuation or quoting as required by PowerShell conventions (the examples above are valid single-line commands in PowerShell as well).

> Tip: use a consistent `--date` or experiment name so logs and checkpoints are easy to locate under `logs/` (see the Model directory section below).

## Inference

### Demo dataset and pretrained weights

A small demo dataset (test movie + ground truth) and two example pretrained weight files are available via Zenodo. This demo allows users to quickly test inference and visualization using our notebooks and scripts. See the `Run_dare3d_Prediction.ipynb` notebook (or the Inference section above) to point to the demo data and run predictions.

### Prediction

We provide `Run_dare3d_Prediction.ipynb`, a Jupyter notebook that guides users through running predictions on their movies. The notebook accepts either:

* A path to your own movies and model checkpoints, or
* The demo data and pretrained weights from Zenodo (recommended for quick testing).

The notebook performs the following:

* Runs the segmentation model to detect division barycenters (the center between two daughter cells).
* Runs the regression model to estimate orientation (angle) and other attributes between daughter cells.
* Exports per-movie visualization outputs (movies and overlays) to your selected output directory.
* Allows interactive comparison with ground truth for qualitative inspection.


### Model directory structure

### Model directory structure

During training, checkpoints and run metadata are written under the repository `logs/` directory. A typical model directory for a single training run follows the structure:

```
logs/
    {training_name}_{folder_name}/        # e.g. segmentation_myDataset or regression_myDataset
        runs/
            {date}/                        # date string passed during training
                checkpoints/
                    epoch_{best_epoch}.ckpt
                    last.ckpt
                .hydra/
                    config.yaml             # training configuration
```

* `training_name` — "segmentation" or "regression"
* `folder_name` — the dataset folder name you supplied via `--set_folder`
* `date` — the experiment date passed during training

When calling `predict.py`, set `model_dir` to the **run directory containing the `checkpoints/` folder**, for example:

```
logs/segmentation_myDataset/runs/2025-05-01/
```

Inside this folder, select a checkpoint from `checkpoints/` (e.g., `epoch_10.ckpt` or `last.ckpt`). The corresponding `.hydra/config.yaml` file in the same run directory is automatically loaded to reconstruct the configuration used during training. You can change the checkpoint folder by modifying the parameter `ckpt_dir`. Check the config file for other overrides: [configs/predict.yaml](configs/predict.yaml)

### Image folder structure

It should be a folder containing `.tif` files which represent the movies you want to infer on.

### Specify the movie scales

In order to infer correctly on your data, you must either provide a json file scale:

```json
{
    "movie_name": [1.0, 1.0, 1.0] # X, Y, Z
}
```

And override the config parameter `+scale_file=<path_to_json>`

Or if the scale is the same across all movies you can override the default scale `+default_scale=1.0` which can be a single scalar or a triplet that represent the scales for X,Y,Z like `+default_scale=[1.0, 1.0, 2.8]`

All scale are supposed to be in μm/voxel

Then you have to specify the target scale `+target_scale=1.0` or `+target_scale=[1.0, 1.0, 0.5]` which will be used to computed the shape of the movie in the target scale.

This is simply done by dividing the movie scale by the target scale to obtain the scale factor that will be used to resize the movie.

For simplicity - we are providing a scales.json file located at `data/3D/` folder for your reference. You could also edit and add your respective movies scales in this file as well.

**Usually a network is trained on a specific target scale so you should only have to specifiy the movie original scale**

### How config loading works

We first load the config from the model dir path `<model_dir>/.hydra/config.yaml` on top of which
we overload parameters by the ones defined in `configs/predict.yaml`. This means that any parameters
that we add in the `configs/predict.yaml` or directly in CLI by adding a parameters (ex: `+data.batch_size=4`) will override the one in the original config.

## Retraining dataset

For retraining, we need:

1. the raw input movie, which should be ordered with the time label first (T,Z,Y,X) and in `.tif` file format.
2. the label movie in the same format as the input movie, with the same dimension as the input movie and must contains labelled daughter cells centers. We retrieve the daughter cells centers pairs by performing a connected component analysis based on the value of the annotations. Two centers belonging to each a daughter cell from the same division must have consecutive label values with the first one being impair and the second pair. For instance, the first daughter cell may have pixels of value 1 and the second daughter cell pixels of value 2.

Then, we expect by default to put these two movies in separate folders like:

```
train/
    im/
        movie.tif
    label/
        movie.tif
    sparse/ (optional)
        movie.tif
```

If you want to add another movie `movie2.tif` and its label `movie2.tif`, you can do so by adding them to each corresponding folders:

```
train/
    im/
        movie.tif
        movie2.tif
    label/
        movie.tif
        movie2.tif
    sparse/ (optional)
        movie.tif
```

The label movie must have the same name as the raw movie.
You can also add a sparse folder which can contains a weight matrix to consider or not specific voxels in a movie. You can rule out certain parts of pixels if you want to. The sparse folder is optional. If a sparse matrix is not in the sparse folder, it defaults to a matrix of one which means that we will use all pixels (no sparse at all) for the given sample.

**If movies are being added, you must add their scale to the `scales.json` file or it will use the default scale.**

## Folder hierarchy

To make the configuration easier it is better if you follow the following folder hierarchy:

```
dare3d/
    data/
        3d/
            movie1/
            movie2/
            movie3/
            exp1/
            exp2/
```

You can generate the experiments by using the two scripts:

* First you need to create split movies on the X axis
  `python scripts/generate_split_movies.py --data_dir=<path to data dir>`
* Then you can generate each experiment
  `python scripts/generate_exp1.py --data_dir=<path to data dir>`

`generate_exp1.py` can range from experiment 1 to 5 example: `generate_exp3.py`.

The data dir is the path where the movie folders are located

You can also generate sparse weight with cylinder shapes by using the script:
`python dare3d/tools/generate_sparse_weights.py --annotated_label <movie.tif>`
