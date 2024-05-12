from typing import List, Tuple
import nltk
import sklearn
from tfidf import TfidfWikiGuesser
import numpy as np
import pandas as pd
from LogRegBuzzer import LogisticRegressionBuzzer


class QuizBowlModel:

    def __init__(self, use_hf_pkl = False):
        """
        Load your model(s) and whatever else you need in this function.

        Do NOT load your model or resources in the guess_and_buzz() function, 
        as it will increase latency severely. 
        """
        #best accuracy when using wiki_page_text.json
        self.guesser = TfidfWikiGuesser(wikidump=None, use_hf_pkl= use_hf_pkl) #can specify different wikidump if needed 
        print("guesser model loaded")

        self.buzzer = LogisticRegressionBuzzer()
        print("buzzer model loaded")


    def guess_and_buzz(self, question_text: List[str]) -> List[Tuple[str, bool]]:
        """
        This function accepts a list of question strings, and returns a list of tuples containing
        strings representing the guess and corresponding booleans representing 
        whether or not to buzz. 

        So, guess_and_buzz(["This is a question"]) should return [("answer", False)]

        If you are using a deep learning model, try to use batched prediction instead of 
        iterating using a for loop.
        """

        answers = []
        top_guesses = 3 #guesser will return this amount guesses for each question (in sorted confidence)

        for question in question_text:
            guesses = self.guesser.make_guess(question, num_guesses=top_guesses)
            # print(f"\n\n\n answered {len(answers)} questions so far \n\n")
            # print(f"left to answer {len(question_text)-len(answers)} questions \n\n ")
            # print(f"progress: {(len(answers)/len(question_text)) * 100} \n\n")

            #do the buzzing 
            buzz = self.buzzer.predict_buzz(question, guesses[0])
            

            #make a tuple and add to answers list 
            tup = (guesses[0], buzz[1])
            print(tup)
            answers.append(tup)

        return answers


        
