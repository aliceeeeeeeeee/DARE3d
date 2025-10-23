<div align="center">

# dare3d on Pytorch

<a href="https://pytorch.org/get-started/locally/"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white"></a>
<a href="https://pytorchlightning.ai/"><img alt="Lightning" src="https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white"></a>
<a href="https://hydra.cc/"><img alt="Config: Hydra" src="https://img.shields.io/badge/Config-Hydra-89b8cd"></a>
<a href="https://github.com/ashleve/lightning-hydra-template"><img alt="Template" src="https://img.shields.io/badge/-Lightning--Hydra--Template-017F2F?style=flat&logo=github&labelColor=gray"></a><br>

</div>

## Description

**DE**ep **L**earning **E**pithelial **T**issue **ME**chanics

This repository contains the Python implementation to detect cell divisions (positions) and their attributes (i.e. angle and length) for 3D images.

### Overview

The approach is devided in two steps:

- Cell division detection using semantic segmentation to detect the center of the division
- Cell attribute regression on detected divisions

This 2 steps approach can be used for 3D images.

## Summary

- [Native installation](#installation)
- [Building singularity image](#building-singularity-images)
- [Download Dataset](#dataset)
- [Pretrained models](#pretrained-models)
- [Inference](#inference)
- [Train on your own data](#train)
- [Run the tests](#tests)
- [Find out here what this project can do](https://github.com/ashleve/lightning-hydra-template)

## Installation

#### Pip

```bash
# clone project
git clone https://github.com/JFRupprecht-OM/DARE3d
git checkout DARE3d
cd DARE3d

# create conda environment
conda create -n dare3d python=3.10
conda activate dare3d

# install requirements
pip install -r requirements.txt
```

## How to run

Train model with default configuration

```bash
# train on CPU
python dare3d3D/train.py experiment=segmentation trainer=cpu

# train on GPU
python dare3d3D/train.py experiment=segmentation trainer=gpu
```

Train model with chosen experiment configuration from [configs/experiment/](configs/experiment/)

```bash
python dare3d3D/train.py experiment=segmentation
```

You can override any parameter from command line like this

```bash
python dare3d3D/train.py experiment=segmentation trainer.max_epochs=20 data.batch_size=64
```

## Building singularity images

## Dataset

## Pretrained Models

## Inference

```bash
python dare3d3D/predict.py model_dir=<path_to_model_dir> inference_dir=<path_to_tif_folder>
```

### Model directory structure

The `model_dir` path must be to the folder containing the checkpoints:

```
/<model_dir>
    /checkpoints
        last.ckpt
    /.hydra
        config.yaml
```

We also make use of the hydra config contained in the `.hydra` folder.
You can change the checkpoint folder by modifying the parameter `ckpt_dir`
Check the config file for other overload [configs/predict.yaml](configs/predict.yaml)

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

**Usually a network is trained on a specific target scale so you should only have to specifiy the movie original scale**

### How config loading works

We first load the config from the model dir path `<model_dir>/.hydra/config.yaml` on top of which
we overload parameters by the ones defined in `configs/predict.yaml`. This means that any parameters
that we add in the `configs/predict.yaml` or directly in CLI by adding a parameters (ex: `+data.batch_size=4`) will override the one in the original config.

### Example of inference with different parameters

This is an example of inference on a folder with tif movies of the same scale.

```bash
python dare3d3D/predict.py\
    model_dir=<path_to_model_dir>\
    inference_dir=<path_to_tif_folder>\
    device=gpu\ # Run the experiment on the gpu
    ckpt_name=scale_1.ckpt\ # Change the name of the model weights in the checkpoints/ folder
    +data.test_data.default_scale="[0.62, 0.62, 2]"
    +data.batch_size=4 # The batch size used for inference
```

## Train

## Tests
