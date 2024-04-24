from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import json

class TfidfWikiGuesser:
    def __init__(self, wikidump = 'resources/wiki_text_16.json') -> None:
        self.tfidf = None 
        self.corpus = None 
        self.titles = None 
        self.vectorizer = None 

        self.load_model(wikidump)

    def load_model(self, wikidump):
        #wiki dump is an json array of json objects with page and text fields 
        with open(wikidump) as f:
            doc = json.load(f)

        self.corpus, self.titles = self.create_corpus(doc)

        self.vectorizer = TfidfVectorizer()
        self.tfidf = self.vectorizer.fit_transform(self.corpus)

    def create_corpus(self, json_file):
        corpus = []
        page_titles = []
        
        for json_obj in json_file:
            corpus.append(json_obj['text'])
            page_titles.append(json_obj['page'])

        return (corpus, page_titles)

    def make_guess(self, question, num_guesses = 1):
        tfidf_question = self.vectorizer.transform([question])

        sim = cosine_similarity(self.tfidf, tfidf_question) 

        #get indices of best matching documents and use it to get (num_guesses) top documents 
        sim_indices = np.argsort(sim.flatten())[::-1]
        best_indices = sim_indices[:num_guesses]
        
        best_docs = []
        best_guesses = []
        for i in best_indices:
            best_docs.append(self.corpus[i])
            best_guesses.append(self.titles[i])

        return best_guesses
        