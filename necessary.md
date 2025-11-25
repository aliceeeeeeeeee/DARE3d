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

# to evaluate

python dare3d/eval.py `
    segmentation.model_dir="C:\Users\tlili\Documents\TRIAL\DARE3d\logs\segmentation3D\runs\2025-11-18_17-12-18-792746" `
    +segmentation.data.batch_size=4 `
    segmentation.threshold=0.1 `
    segmentation.min_weighted_prob=0.6 `
    segmentation.ckpt_name=epoch_164.ckpt `
    regression.model_dir="C:\Users\tlili\Documents\TRIAL\DARE3d\logs\regression3D\runs\2025-11-19_09-37-06-929606" `
    regression.ckpt_name=epoch_084.ckpt `
    +regression.data.batch_size=1 
    
for gastruloids - RuntimeError: Calculated padded input size per channel: (34 x 2 x 34). Kernel size: (3 x 3 x 3). Kernel size can't be greater than actual input size

Evaluating...:   0%|                                                                                                                                                  | 0/1 [00:00<?, ?it/s]C:\Users\tlili\Documents\DARE3d\dare3D\metrics\object_level.py:76: NumbaTypeSafetyWarning: unsafe cast from float64 to float32. Precision may be lost.
  prob[value] = 0.0
C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\skimage\_shared\utils.py:328: UserWarning: C:\Users\tlili\Documents\DARE3d\logs\segmentation3D\runs\2025-11-14_12-00-13-297772\movie4\movie4_true.tif is a low contrast image
  return func(*args, **kwargs)
C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\skimage\_shared\utils.py:328: UserWarning: C:\Users\tlili\Documents\DARE3d\logs\segmentation3D\runs\2025-11-14_12-00-13-297772\movie4\movie4_pred.tif is a low contrast image
  return func(*args, **kwargs)
C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\skimage\_shared\utils.py:328: UserWarning: C:\Users\tlili\Documents\DARE3d\logs\segmentation3D\runs\2025-11-14_12-00-13-297772\movie4\movie4_fp.tif is a low contrast image
  return func(*args, **kwargs)
C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\skimage\_shared\utils.py:328: UserWarning: C:\Users\tlili\Documents\DARE3d\logs\segmentation3D\runs\2025-11-14_12-00-13-297772\movie4\movie4_fn.tif is a low contrast image
  return func(*args, **kwargs)
[2025-11-14 17:40:43,361][dare3D.data.dare_datamodule][INFO] - [rank: 0] Setting augmentations...
[2025-11-14 17:40:43,386][__main__][INFO] - [rank: 0] Instantiating loggers...
[2025-11-14 17:40:43,386][dare3D.utils.instantiators][INFO] - [rank: 0] Instantiating logger <lightning.pytorch.loggers.mlflow.MLFlowLogger>
[2025-11-14 17:40:43,388][dare3D.utils.instantiators][INFO] - [rank: 0] Instantiating logger <lightning.pytorch.loggers.tensorboard.TensorBoardLogger>
[2025-11-14 17:40:43,389][dare3D.utils.instantiators][INFO] - [rank: 0] Instantiating logger <dare3D.loggers.regression_logger.RegressionLogger>
[2025-11-14 17:40:43,390][__main__][INFO] - [rank: 0] Loading checkpoint: C:\Users\tlili\Documents\DARE3d\logs\regression3D\runs\2025-11-14_16-31-28-967813\checkpoints\epoch_094.ckpt       
C:\Users\tlili\Documents\DARE3d\dare3D\eval.py:129: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  state_dict = torch.load(cfg.ckpt_path, map_location="cpu")["state_dict"]
[2025-11-14 17:40:43,437][dare3D.data.components.abstract_celldataset][INFO] - Loading all movies and bipoints...
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:08<00:00,  8.57s/it]
[2025-11-14 17:40:52,011][dare3D.data.components.abstract_celldataset][INFO] -  LOADED 1 movies with a total of 10 timestamps
[2025-11-14 17:40:52,078][dare3D.data.components.abstract_celldataset][INFO] - Total number of sequences: 8
Padding 1 movies...: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.08it/s]
[2025-11-14 17:40:53,026][dare3D.data.components.cell_3dataset][INFO] - Normalizing all movies using renorm=min-max
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.43s/it]
Number of matched centers : 220
Using GPU
Prediction will be stored in folder: C:\Users\tlili\Documents\DARE3d\logs\regression3D\runs\2025-11-14_16-31-28-967813\pred_centers
Running regression inference...:   1%|█▌                                                                                                                    | 3/220 [00:01<01:33,  2.33it/s] 
Error executing job with overrides: ['segmentation.model_dir=C:\\Users\\tlili\\Documents\\DARE3d\\logs\\segmentation3D\\runs\\2025-11-14_12-00-13-297772', '+segmentation.data.batch_size=4', 'segmentation.threshold=0.1', 'segmentation.min_weighted_prob=0.6', 'segmentation.ckpt_name=epoch_125.ckpt', 'regression.model_dir=C:\\Users\\tlili\\Documents\\DARE3d\\logs\\regression3D\\runs\\2025-11-14_16-31-28-967813', 'regression.ckpt_name=epoch_094.ckpt', '+regression.data.batch_size=1']
Traceback (most recent call last):
  File "C:\Users\tlili\Documents\DARE3d\dare3D\eval.py", line 228, in <module>
    main()
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\hydra\main.py", line 94, in decorated_main
    _run_hydra(
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\hydra\_internal\utils.py", line 394, in _run_hydra
    _run_app(
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\hydra\_internal\utils.py", line 457, in _run_app
    run_and_report(
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\hydra\_internal\utils.py", line 223, in run_and_report
    raise ex
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\hydra\_internal\utils.py", line 220, in run_and_report
    return func()
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\hydra\_internal\utils.py", line 458, in <lambda>
    lambda: hydra.run(
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\hydra\_internal\hydra.py", line 132, in run
    _ = ret.return_value
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\hydra\core\utils.py", line 260, in return_value
    raise self._return_value
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\hydra\core\utils.py", line 186, in run_job
    ret.return_value = task_function(task_cfg)
  File "C:\Users\tlili\Documents\DARE3d\dare3D\eval.py", line 225, in main
    evaluate(segmentation_cfg, regression_cfg)
  File "C:\Users\tlili\Documents\DARE3d\dare3D\eval.py", line 173, in evaluate
    reg_stats = evaluate_regression(reg_cfg, info)
  File "C:\Users\tlili\Documents\DARE3d\dare3D\eval.py", line 142, in evaluate_regression
    stats = infer_and_evaluate_regression(dataset=datamodule.data_test,
  File "C:\Users\tlili\Documents\DARE3d\dare3D\metrics\infer_measure.py", line 283, in infer_and_evaluate_regression
    pred_angle_length = regression_inference(
  File "C:\Users\tlili\Documents\DARE3d\dare3D\metrics\inference.py", line 125, in regression_inference
    y = model.forward(X)
  File "C:\Users\tlili\Documents\DARE3d\dare3D\models\components\simple_regression_net.py", line 72, in forward
    features = block(features)
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\torch\nn\modules\module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\torch\nn\modules\module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
  File "C:\Users\tlili\Documents\DARE3d\dare3D\models\components\simple_regression_net.py", line 17, in forward
    x = self.conv1(x)
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\torch\nn\modules\module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\torch\nn\modules\module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\torch\nn\modules\conv.py", line 725, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "C:\Users\tlili\AppData\Local\anaconda3\envs\dare3d\lib\site-packages\torch\nn\modules\conv.py", line 720, in _conv_forward
    return F.conv3d(
RuntimeError: Calculated padded input size per channel: (34 x 2 x 34). Kernel size: (3 x 3 x 3). Kernel size can't be greater than actual input size

# to predict

python dare3D/predict.py -m `
    segmentation.model_dir="C:\Users\tlili\Documents\DARE3d\logs\segmentation3D\runs\2025-11-10_11-04-41-140511" `
    segmentation.ckpt_name=epoch_045.ckpt `
    segmentation.threshold=0.5,0.8 `
    segmentation.min_weighted_prob=0.1,0.4 `
    segmentation.inference_overlap=0.25 `
    inference_dir=dare_data\test_input
    regression.model_dir="C:\Users\tlili\Documents\DARE3d\logs\regression3D\runs\2025-11-06_17-40-27-423287" `
    regression.ckpt_name=epoch_003.ckpt