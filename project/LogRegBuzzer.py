from sklearn.linear_model import LogisticRegression
import joblib
from huggingface_hub import hf_hub_download
from transformers import pipeline
import pandas as pd 


class LogisticRegressionBuzzer:

    def __init__(self) -> None:
        self.model = self.load_from_hf_pkl()
        self.features = BuzzerFeatures()


    def load_from_hf_pkl(self) -> LogisticRegression:
        REPO_ID = "nes470/pipeline-as-repo"
        FILENAME = "logreg_buzzer_model.pkl"

        model = joblib.load(
            hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
        )

        return model 
    
    def predict_buzz(self, question, guess):
        X = self.features.get_features(question, guess)

        X_formatted = pd.DataFrame(X, index=[0])
        pred = self.model.predict(X_formatted)

        print(pred)
        #use predict_proba to get confidence probabilities 
        prob_pred = self.model.predict_proba(X_formatted)
        print(prob_pred)

        return (pred, prob_pred[0][1])
    

    

class BuzzerFeatures:
    def __init__(self) -> None:
        self.ner =  pipeline("ner")

    #returns dict with all the features 
    def get_features(self, question, guess):
        sent_count = self.sentence_count(question)
        guess_word_count = self.guess_word_count(guess)
        guess_has_paren = self.guess_has_paren(guess)
        guess_length = self.guess_length(guess)
        guess_entity = self.guess_entity(guess)
        
        feats = {'sentence_count':sent_count, 'guess_word_count':guess_word_count,
              'guess_has_paren':guess_has_paren, 'guess_length':guess_length}
        
        X = feats | guess_entity

        return X 




    def sentence_count(self, str):
        return len(str.split("."))

    def guess_word_count(self, str):
        return len(str.split("_"))

    def guess_has_paren(self, str):
        return int("(" in str or ")" in str)

    def guess_length(self, str):
        return len(str)
    
    def guess_entity(self, text):
        entities = self.ner(text)
        if len(entities) == 0:
            type =  ""  # <-- use "None" instead TODO
        else:
            type = entities[0]["entity"]

        if type == "":
            return {'':1, 'I-LOC':0, 'I-MISC':0, 'I-ORG':0, 'I-PER':0}
        if type == "I-LOC":
            return {'':0, 'I-LOC':1, 'I-MISC':0, 'I-ORG':0, 'I-PER':0}
        if type == "I-MISC":
            return {'':0, 'I-LOC':0, 'I-MISC':1, 'I-ORG':0, 'I-PER':0}
        if type == "I-ORG":
            return {'':0, 'I-LOC':0, 'I-MISC':0, 'I-ORG':1, 'I-PER':0}
        if type == "I-PER":
            return {'':0, 'I-LOC':0, 'I-MISC':0, 'I-ORG':0, 'I-PER':1}
            

