from QBModelConfig import QBModelConfig
from QBModelWrapper import QBModelWrapper
import torch 

qbmodel_config = QBModelConfig()
qbmodel = QBModelWrapper(qbmodel_config)

qbmodel.push_to_hub("quiz-bowl-model")
#qbmodel.save_pretrained(save_directory='hf-model-save', safe_serialization=False, state_dict=None)