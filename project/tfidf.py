from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


def create_corpus(json_file):
    corpus = []
    page_titles = []
    
    for json_obj in json_file:
        corpus.append(json_obj['text'])
        page_titles.append(json_obj['page'])


    return (corpus, page_titles)


#wiki dump is an json array of json objects with page and text fields 
with open('resources/wiki_text_16.json') as f:
    doc = json.load(f)

corpus, titles = create_corpus(doc)

vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(corpus)

question = "An object orbiting this planet contains sections named Liberty, Equality, and Fraternity. A small group of clouds on this planet was nicknamed \"the Scooter\" for its high speed. Volcanoes that eject ice were first observed on an object that orbits this planet. The first high resolution images of this object were taken by Voyager 2 and revealed a storm system known as the \"Great Dark Spot\". Johann Galle first observed this planet from a telescope using predictions made by Urbain Le Verrier [\"ur-BAIN le vay-ree-AY\"] about its effects on the orbit of Uranus. For 10 points, name this dark blue gas giant, the outermost planet in the Solar System."
tfidf_question = vectorizer.transform([question])

sim = cosine_similarity(tfidf, tfidf_question) 

#get index of best matching document and use it to get sim document 
sim_index = sim.argmax()
sim_doc = corpus[sim_index]

print(titles[sim_index])
# print(corpus[sim_index])