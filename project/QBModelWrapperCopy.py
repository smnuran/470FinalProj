from typing import List
from transformers import PreTrainedModel
from transformers import PretrainedConfig
from QBModelConfig import QBModelConfig
from qbmodel import QuizBowlModel

class QBModelWrapper(PreTrainedModel):
    config_class= QBModelConfig


    def __init__(self, config):
        super().__init__(config)

        self.model = QuizBowlModel(use_hf_pkl=True)
        self.tfmodel = self.model.guesser

    
    def forward(self, question, context):
        output = self.model.guess_and_buzz([question])
        return output[0]
