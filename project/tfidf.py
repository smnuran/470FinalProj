from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import json
import zipfile
import pickle
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from huggingface_hub import hf_hub_download
import joblib


class TfidfWikiGuesser:
    def __init__(self, wikidump = 'resources/wiki_text_16.json', use_hf_pkl = False) -> None:
        self.tfidf = None 
        self.corpus = None 
        self.titles = None 
        self.vectorizer = None 
        self.lemmatizer = WordNetLemmatizer()
        model_file = "processed_tfidf_wiki_page_text_model.pkl" # <--- has best acc so far (using wiki_page_text.json from gdrive folder)
        #model_file = "processed_large_wiki_text_model.pkl"
        #model_file = "processed_tfidf_wiki_16_model.pkl"
        # full_model_path = model_file
        full_model_path = os.path.join("./models", model_file)

        if(use_hf_pkl):
            REPO_ID = "nes470/pipeline-as-repo"
            FILENAME = "processed_tfidf_wiki_page_text_model.pkl"

            model = joblib.load(
                hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
            )
            
        
            print("loading from hugginface pkl file")
            self.load_from_pk_direct(model)
        else:
            if os.path.exists(full_model_path):
                print("Loading model from pickle...")
                self.load_from_pkl(full_model_path)
            else:
                if wikidump:
                    print("No pre-trained model found, loading data from dump...")
                    self.load_model(wikidump)
                    self.save_model(full_model_path)
        # self.load_model(wikidump)

    def load_model(self, wikidump):
        # wiki dump is an json array of json objects with page and text fields 
        with open(wikidump) as f:
            doc = json.load(f)
        # with zipfile.ZipFile('resources/wiki_text_8.json.zip', 'r') as z:
        #     with z.open('wiki_text_8.json') as f:
        #         doc = json.load(f)


        self.corpus, self.titles = self.create_corpus(doc)

        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf = self.vectorizer.fit_transform(self.corpus)

    def preprocess_text(self,text):
        if type(text) == float:
            return str(text)
        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]
        processed_text = ' '.join(lemmatized_tokens)
        return processed_text

    def create_corpus(self, json_file):
        corpus = []
        page_titles = []
        
        for json_obj in json_file:
            # corpus.append(json_obj['text'])
            #corpus.append(self.preprocess_text(json_obj['text']))
            corpus.append(json_obj['text'])
            page_titles.append(json_obj['page'])

        return (corpus, page_titles)

    def make_guess(self, question, num_guesses = 1):
        tfidf_question = self.vectorizer.transform([question])

        sim = cosine_similarity(self.tfidf, tfidf_question) 

        #get indices of best matching documents and use it to get (num_guesses) top documents 
        sim_indices = np.argsort(sim.flatten())[::-1]
        best_indices = sim_indices[:num_guesses]
        
        # best_docs = []
        best_guesses = []
        cos_sim_scores = []
        for i in best_indices:
            # best_docs.append(self.corpus[i])
            best_guesses.append(self.titles[i])
            cos_sim_scores.append(sim[[i], 0])

        return best_guesses, cos_sim_scores
        
    def save_model(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'tfidf_matrix': self.tfidf,
                'titles': self.titles,
                # 'corpus': self.corpus
            }, f)

    def load_from_pkl(self, file_name):
        with open(file_name, 'rb') as f:
            data = pickle.load(f)
            self.vectorizer = data['vectorizer']
            self.tfidf = data['tfidf_matrix']
            self.titles = data['titles']
            # self.corpus = data['corpus']

    def load_from_pk_direct(self, pkl):
        #data = pickle.load(pkl)
        data = pkl
        self.vectorizer = data['vectorizer']
        self.tfidf = data['tfidf_matrix']
        self.titles = data['titles']