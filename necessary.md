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

pip install numpy==1.23.4 numba==0.59
RUN THESE IN POWERSHELL

# 1) Activate your environment first (example for conda)
conda activate dare3d

# 2) Then install all other packages from requirements.txt
pip install -r requirements.txt

# 3) Install PyTorch + CUDA wheel (run this BEFORE pip installing the requirements)
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4) Set HYDRA_FULL_ERROR=1 for this session (PowerShell)
[$Env:HYDRA_FULL_ERROR = "1"](.) this and pip install -e. - everytime new folder $Env:HYDRA_FULL_ERROR = "1"

# 5) Verify the env var is set (visual check)
echo $Env:HYDRA_FULL_ERROR
# should print: 1





python dare3d/predict.py `
segmentation.model_dir=C:\Users\Qazi\Documents\PhD_Y1\Division3D\DARE3d\dare_data\weights\segmentation3d_exp10-b `
regression.model_dir=C:\Users\Qazi\Documents\PhD_Y1\Division3D\DARE3d\dare_data\weights\regression3d_exp10-b `
inference_dir=C:\Users\Qazi\Documents\PhD_Y1\Division3D\DARE3d\dare_data\test_input  `.


# for segmentation retraining

python dare3D/train.py `
    experiment=segmentation `
    data.batch_size=24 `
    train_dir="3D/train" `
    val_dir="3D/val" `
    test_dir="3D/test" `
    trainer.max_epochs=200 `
    model.optimizer.lr=0.1 `
    model/scheduler=one_cycle_lr `
    model.scheduler_interval="step" `
    +segmentation.logger.mlflow.tracking_uri="file:///C:/Users/tlili/Documents/DARE3d/logs/mlflow/mlruns"

# for regression retraining

python dare3D/train.py `
    experiment=regression `
    steps_per_epoch=1000 `
    model.optimizer.lr=0.001 `
    data.batch_size=32 `
    train_dir="3D/train" `
    val_dir="3D/val" `
    model/net=simple_regression_net `
    model.net.n_stages=3 `
    model.net.start_filters=32 

# Errors faced while using mlflow -
full_key: logger.mlflow
KeyError: 'c'

"C:\Users\tlili\Documents\DARE3d\configs\logger\mlflow.yaml" - change to file:///C:/Users/tlili/Documents/DARE3d/configs/logger/mlflow.yaml

in mlflow.yaml - tracking_uri: ${paths.log_dir}/mlflow/mlruns changed to tracking_uri: "file:///${paths.log_dir}/mlflow/mlruns" because thats how it is described in the inria notes by romain.

need to make the folders mlflow/mlruns in dare3d/logs



# I commented the mlflow.yaml - to run
# only relative paths work
# the scale has to be of 3 dimensions during retraining
# test also needs a labels folder
# conda init powershell- necessary when (base) and (dare3d) dont show up in the command prompt.
# scales of images of mehdi is [TZYX] is as [1.0,1.0,0.2076,0.2076]
# in scales.json file - the order of the scales is X,Y,Z
# 

# for regression retrain - changes made in regress_logger(data/loggers) and regress_3dataset.py(data/components) _ as qazi_change

# in notebook code
---> 30 for line in process.stdout:
     31     sys.stdout.write(line)

File c:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\encodings\cp1252.py:23, in IncrementalDecoder.decode(self, input, final)
     22 def decode(self, input, final=False):
---> 23     return codecs.charmap_decode(input,self.errors,decoding_table)[0]

UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 41: character maps to <undefined>

segmentation_model_dir = r"C:\Users\tlili\Documents\DARE3d\logs\segmentation3D\runs\2025-11-10_11-04-41-140511"
regression_model_dir   = r"C:\Users\tlili\Documents\DARE3d\logs\regression3D\runs\2025-11-06_17-40-27-423287"

# to train and evaluate 

use the train_eval.py. 

Case 1: Doing both segmentation and regression as well as eval

Case 2: Only segmentation training and evaluation
   python dare3d/train_eval.py --set_folder <your_folder_name> --epoch <number_of_epochs> --date <date_of_the_experiment>--train_segmentation True --train_regression False

Case 3: Only regression training and evaluation
   python dare3d/train_eval.py --set_folder <your_folder_name> --epoch <number_of_epochs> --date <date_of_the_experiment>--train_segmentation True --train_regression False

Case 4: Only evaluation
   python dare3d/train_eval.py --set_folder <your_folder_name> --epoch <number_of_epochs> --date <date_of_the_experiment>--train_segmentation True --train_regression False
    
