from transformers import PretrainedConfig

class QBModelConfig(PretrainedConfig):
    model_type = 'QA'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

