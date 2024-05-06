to run: 

python3 testqb.py 

inside the testqb file you can configure the limit for num questions to set (current default is limit=2000) 


hugging-face model at: nes470/pipeline-as-repo

inference example: 

from transformers import pipeline

qa_pipe = pipeline(model="nes470/new-attempt-pipeline-2", trust_remote_code=True)
res = qa_pipe(question="This star has 8 planets in it's solar system?", context="context to the question")
print(res)
