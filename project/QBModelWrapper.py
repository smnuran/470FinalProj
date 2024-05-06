from typing import List
from transformers import PreTrainedModel
from transformers.configuration_utils import PretrainedConfig
from QBModelConfig import QBModelConfig
from qbmodel import QuizBowlModel

class QBModelWrapper(PreTrainedModel):
    config_class= QBModelConfig

    # def __init__(self, config: PretrainedConfig, *inputs, **kwargs):
    #     super().__init__(config, *inputs, **kwargs)

    #     self.model = QuizBowlModel()


    def __init__(self, config):
        super().__init__(config)

        self.model = QuizBowlModel()

    
    #def forward
    def forward(self, question):
        self.model.guess_and_buzz(question)
