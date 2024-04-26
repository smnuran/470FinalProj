from typing import List, Tuple
import nltk
import sklearn
from tfidf import TfidfWikiGuesser
import numpy as np
import pandas as pd


class QuizBowlModel:

    def __init__(self):
        """
        Load your model(s) and whatever else you need in this function.

        Do NOT load your model or resources in the guess_and_buzz() function, 
        as it will increase latency severely. 
        """
        
        self.guesser = TfidfWikiGuesser() #can specify different wikidump if needed 
        print("model loaded")



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
            #print(guesses)

            #do the buzzing 

            #make a tuple and add to answers list 
            tup = (guesses[0], True)
            answers.append(tup)

        return answers


        
