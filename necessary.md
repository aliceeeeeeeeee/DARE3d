# --------- pytorch --------- #
torch>=2.0.0
torchvision>=0.15.0
lightning>=2.0.0
torchmetrics>=0.11.4

# --------- hydra --------- #
hydra-core==1.3.2
hydra-colorlog==1.2.0
hydra-optuna-sweeper==1.2.0

# --------- loggers --------- #
mlflow
tensorboard

# --------- others --------- #
rootutils
pre-commit
rich
pytest

# --------- dl library ----- #
monai==1.3.0

# ------ image processing --- #
scikit-image
augmend
gputools
scikit-tensor-py3

# Display
napari
einops

torchgeometry
numba==0.59
numpy==1.23.4


RUN THESE IN POWERSHELL

# 1) Activate your environment first (example for conda)
conda activate dare3d

# 2) Set HYDRA_FULL_ERROR=1 for this session (PowerShell)
[$Env:HYDRA_FULL_ERROR = "1"](.) this and pip install -e. - everytime new folder

# 3) Verify the env var is set (visual check)
echo $Env:HYDRA_FULL_ERROR
# should print: 1

# 4) Install PyTorch + CUDA wheel (run this BEFORE pip installing the requirements)
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 5) Then install all other packages from requirements.txt
pip install -r requirements.txt

$Env:HYDRA_FULL_ERROR = "1"
python deletme3d/predict.py `
segmentation.model_dir=C:\Users\Qazi\Documents\PhD_Y1\Division3D\DARE3d\dare_data\weights\segmentation3d_exp10-b `
regression.model_dir=C:\Users\Qazi\Documents\PhD_Y1\Division3D\DARE3d\dare_data\weights\regression3d_exp10-b `
inference_dir=C:\Users\Qazi\Documents\PhD_Y1\Division3D\DARE3d\dare_data\test_input  `

python deletme3D/train.py `
    experiment=segmentation `
    data.batch_size=24 `
    train_dir="3D/train" `
    val_dir="3D/val" `
    test_dir="3D/test" `
    trainer.max_epochs=200 `
    model.optimizer.lr=0.1 `
    model/scheduler=one_cycle_lr `
    model.scheduler_interval="step"

# I commented the mlflow.yaml - to run
# only relative paths work
# the scale has to be of 3 dimensions during retraining
# test also needs a labels folder
