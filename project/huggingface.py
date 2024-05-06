from QBModelConfig import QBModelConfig
from QBModelWrapper import QBModelWrapper
from transformers import AutoConfig, AutoModel, AutoModelForQuestionAnswering
import torch 
import numpy as np
from transformers import QuestionAnsweringPipeline
from transformers.pipelines import PIPELINE_REGISTRY
from transformers import AutoModelForQuestionAnswering, TFAutoModelForQuestionAnswering
from transformers import pipeline



class DemoQAPipeline(QuestionAnsweringPipeline):
    def postprocess(self, model_outputs):
        answers = super().postprocess(model_outputs)
        return {'guess': answers['answer'], 'confidence': answers['score']}


AutoConfig.register("QA-umd-quizbowl", QBModelConfig)
AutoModel.register(QBModelConfig, QBModelWrapper)
AutoModelForQuestionAnswering.register(QBModelConfig, QBModelWrapper)

QBModelConfig.register_for_auto_class()
QBModelWrapper.register_for_auto_class("AutoModel")
QBModelWrapper.register_for_auto_class("AutoModelForQuestionAnswering")

PIPELINE_REGISTRY.register_pipeline(
    "demo-qa",
    pipeline_class=DemoQAPipeline,
    pt_model=AutoModelForQuestionAnswering,
    tf_model=TFAutoModelForQuestionAnswering,
)



qbmodel_config = QBModelConfig()
qbmodel = QBModelWrapper(qbmodel_config)

# # qbmodel_config.save_pretrained("hf-model-config")
qbmodel.save_pretrained(save_directory='hf-model-save', safe_serialization= False,
                        push_to_hub=True)
# qbmodel.push_to_hub("quiz-bowl-model-qa-new-attempt")

model = AutoModelForQuestionAnswering.from_pretrained("nes470/hf-model-save", trust_remote_code = True)
qa_pipe = pipeline("question-answering", model=model)

