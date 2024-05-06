from transformers import PretrainedConfig
import torch

class QBModelConfig(PretrainedConfig):
    model_type = 'QA-umd-quizbowl'

    def __init__(self, **kwargs):
        self.torch_dtype = torch.float16
        super().__init__( **kwargs)
        

