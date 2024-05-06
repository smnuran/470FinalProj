from transformers import Pipeline
from transformers import PreTrainedTokenizer
from transformers.utils import ModelOutput

from transformers import PreTrainedModel, Pipeline
from typing import Any, Dict, List

class QApipeline(Pipeline):
    def __init__(
        self,
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        **kwargs
    ):
        super().__init__(
            model=model,
            **kwargs
        )

        print("in __init__")

    def __call__( self, question: str,  context: str, **kwargs) -> Dict[str, Any]:
        inputs = {
            "question": question,
            "context": context
        }

        outputs = self.model(**inputs)

        answer = self._process_output(outputs)

        print("in __call___")

        return answer 

    def _process_output(self, outputs: Any) -> str:

        print("in process outputs")

        format =  {'guess': outputs[0], 'confidence': int(outputs[1])}
        return format

    
    def _sanitize_parameters(self, **kwargs):
        print("in sanatize params")

        return {}, {}, {}

    def preprocess(self, inputs):
        print("in preprocess")

        return inputs

    def postprocess(self, outputs):
        print("in postprocess")
        format =  {'guess': outputs[0], 'confidence': float(outputs[1])}
        return format
    
    def _forward(self, input_tensors, **forward_parameters: Dict) -> ModelOutput:
        print("in _forward")
        return super()._forward(input_tensors, **forward_parameters)
    