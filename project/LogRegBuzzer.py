from sklearn.linear_model import LogisticRegression
import joblib
from huggingface_hub import hf_hub_download
from transformers import pipeline
import pandas as pd 


class LogisticRegressionBuzzer:

    def __init__(self) -> None:
        self.model = self.load_from_hf_pkl()
        self.features = BuzzerFeatures()
        self.df = None 


    def load_from_hf_pkl(self) -> LogisticRegression:
        REPO_ID = "nes470/pipeline-as-repo"
        FILENAME = "logreg_buzzer_balanced_extra_model.pkl"

        model = joblib.load(
            hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
        )

        return model 
    
    def predict_buzz(self, question, guess, sim_score):
        X = self.features.get_features(question, guess)
        sim_score = {'sim_score':sim_score, 'question':question}
        csv_dict_X = X | sim_score

        csv_df = pd.DataFrame(csv_dict_X)
        if self.df is None:
            self.df = csv_df
        else:
            self.df = pd.concat([self.df, csv_df])


        X_formatted = X | csv_dict_X
        X_formatted = pd.DataFrame(X_formatted, index=[0])
        X_df = X_formatted[["sentence_count","guess_word_count", "guess_has_paren", "guess_length",
                             "sim_score", "I-LOC", "I-MISC", "I-ORG", "I-PER"]]
        
        pred = self.model.predict(X_df)

        #print(pred)
        #use predict_proba to get confidence probabilities 
        prob_pred = self.model.predict_proba(X_df)
        #print(prob_pred)

        buzz_confidence = self.confidence(prob_pred[0][1], threshold=.8)
        #print(buzz_confidence)

        return (pred, buzz_confidence)
    
    #prob is (true) predict prob 
    def confidence(self, prob, threshold):
        #try buzzing if only above threshold otherwise make it low. 
        multiplier = .3
        if prob > threshold:
            return prob 
        elif prob < (threshold/2):
            return multiplier * prob 
        else:
            #so these nums somewhere in middle , wanna make it still low 
            return multiplier * 2 * prob
        


    

    

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
        if str is None or str == "":
            return 0
        return len(str.split("."))

    def guess_word_count(self, str):
        if str is None or str == "":
            return 0
        return len(str.split("_"))

    def guess_has_paren(self, str):
        if str is None or str == "":
            return 0 
        return int("(" in str or ")" in str)

    def guess_length(self, str):
        if str is None or str == "":
            return 0
        return len(str)
    
    def guess_entity(self, text):
        if text is None or text == "":
            return {'':1, 'I-LOC':0, 'I-MISC':0, 'I-ORG':0, 'I-PER':0}

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
            

