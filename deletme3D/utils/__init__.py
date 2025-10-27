from deletme3D.utils.instantiators import instantiate_callbacks, instantiate_loggers
from deletme3D.utils.logging_utils import log_hyperparameters
from deletme3D.utils.pylogger import RankedLogger
from deletme3D.utils.rich_utils import enforce_tags, print_config_tree
from deletme3D.utils.utils import extras, get_metric_value, task_wrapper

from lightning.pytorch.plugins.environments import SLURMEnvironment
from torch import nn

class DisabledSLURMEnvironment(SLURMEnvironment):
    def detect() -> bool:
        return False

    @staticmethod
    def _validate_srun_used() -> None:
        return

    @staticmethod
    def _validate_srun_variables() -> None:
        return
    
class ModelOutputWrapper(nn.Module):
    def __init__(self, model, f):
        super().__init__()
        self.model = model
        self.f = f
    def forward(self, x):
        o = self.model(x)
        return self.f(o)
    
class CriterionWrapper(nn.Module):
    def __init__(self, criterion, f):
        super().__init__()
        self.criterion = criterion
        self.f = f
        
    def forward(self, x, y):
        loss = self.criterion(x, y)
        return self.f(loss)