import string
from typing import Counter
from qbmodel import QuizBowlModel
import json 
import pandas as pd 
import time 
import random 


def normalize_answer(answer):
    """
    Remove superflous components to create a normalized form of an answer that
    can be more easily compared.
    """
    from unidecode import unidecode
    
    if answer is None:
        return ''
    reduced = unidecode(answer)
    reduced = reduced.replace("_", " ")
    if "(" in reduced:
        reduced = reduced.split("(")[0]
    reduced = "".join(x for x in reduced.lower() if x not in string.punctuation)
    reduced = reduced.strip()

    for bad_start in ["the ", "a ", "an "]:
        if reduced.startswith(bad_start):
            reduced = reduced[len(bad_start):]
    return reduced.strip()
 
def rough_compare(guess, page):
    """
    See if a guess is correct.  Not perfect, but better than direct string
    comparison.  Allows for slight variation.
    """
    if page is None:
        return False
    
    guess = normalize_answer(guess)
    page = normalize_answer(page)

    if guess == '':
        return False
    
    if guess == page:
        return True
    elif page.find(guess) >= 0 and (len(page) - len(guess)) / len(page) > 0.5:
        return True
    else:
        return False

def compare_answers(str1: str, str2: str):
    stripped_1 = ''.join(c.lower() for c in str1 if not c.isspace())
    stripped_2 = ''.join(c.lower() for c in str2 if not c.isspace())


    if stripped_1 == stripped_2:
          return True 
    
    if stripped_1.find(stripped_2) != -1:
          return True 
    
    if stripped_2.find(stripped_1) != -1:
          return True 
    
    stripped_1 = stripped_1.replace("_", "")
    stripped_1 = stripped_1.replace("-", "")
    stripped_2 = stripped_2.replace("_", "")
    stripped_2 = stripped_2.replace("-", "")

    strip = [',','[',']','{','}', '.', '!', '(', ')', ';', ':', '\'',"\""]
    stripped_1  = stripped_1.translate({ord(c): '' for c in strip})
    stripped_2 = stripped_2.translate({ord(c): '' for c in strip})

    if stripped_1 == stripped_2:
          return True 
    
    if stripped_1.find(stripped_2) != -1:
          return True 
    
    if stripped_2.find(stripped_1) != -1:
          return True 

    return False



qb = QuizBowlModel(use_hf_pkl=True)

question = '''An object orbiting this planet contains sections named Liberty, Equality, and Fraternity.
 A small group of clouds on this planet was nicknamed \"the Scooter\" for its high speed. 
 Volcanoes that eject ice were first observed on an object that orbits this planet.
 The first high resolution images of this object were taken by Voyager 2 and revealed a storm system known as the \"Great Dark Spot\".
 Johann Galle first observed this planet from a telescope using predictions made by Urbain Le Verrier [\"ur-BAIN le vay-ree-AY\"] about its effects on the orbit of Uranus.
 For 10 points, name this dark blue gas giant, the outermost planet in the Solar System.
'''


#can split question into chunks to see how guesser works on harder difficulty. 
def get_splits(question: str):
      splits = question.split(".")
      full_str = ""
      result_chunks = []
      #each split should get longer with each iteration adding upto full question
      for split in splits:
            full_str = full_str + "." + split 
            result_chunks.append(full_str)
            #print(full_str + "\n")
      
      return result_chunks


data_source = 'resources/small.buzztrain.json'
with open(data_source) as f:
            doc = json.load(f)
questions_json = doc['questions']
questions = []
answers = []
limit = 100 #only test this many or less questions 
test_splits = True 
for x in range(limit):

      question_json = random.choice(questions_json)
      

      if test_splits:
            #if you want to test question splits: 
            splits = get_splits(question_json['text'])
            #print(splits)

            for q in splits:
                  if q is not None and q != "":
                        questions.append(q)
                        answers.append(question_json["answer"])              
      else:
            question = question_json['text']
            answer = question_json['answer']
            questions.append(question)
            answers.append(answer)





#questions = # splits #[question]
result = qb.guess_and_buzz(questions)
correct = 0 

guesses = []
buzz = []
correct_answer = []
buzz_result = []
confidence = Counter()
for idx, (result_answer, result_buzz) in enumerate(result): 
        if result_answer is None or answers[idx] is None:
            result_answer = "NONE"
            print(f"abandoned: {result_answer} or {answers[idx]}")
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(False)
            buzz_result.append(result_buzz)
        elif rough_compare(result_answer, answers[idx]):
            correct += 1 
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(True)
            buzz_result.append(result_buzz)
            if result_buzz:
                 confidence["best(good)"] += 1 
            else:
                 confidence["scared_to_buzz"] += 1

        elif answers[idx] == result_answer:
            correct += 1 
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(True)
            buzz_result.append(result_buzz)
            if result_buzz:
                 confidence["best(good)"] += 1 
            else:
                 confidence["scared_to_buzz"] += 1
            #print("correct | question: " + questions[idx] + " | answer: " + result_answer)
        elif answers[idx].find(result_answer) != -1:
            #print("almost | correct answer: " + answers[idx] + " | result: " + result_answer)
            correct += 1
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(True)
            buzz_result.append(result_buzz)
            if result_buzz:
                 confidence["best(good)"] += 1 
            else:
                 confidence["scared_to_buzz"] += 1
        elif compare_answers(result_answer, answers[idx]):
            correct += 1
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(True)
            buzz_result.append(result_buzz)
            if result_buzz:
                 confidence["best(good)"] += 1 
            else:
                 confidence["scared_to_buzz"] += 1
        else:
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(False)
            buzz_result.append(result_buzz)
            if result_buzz:
                 confidence["aggressive_buzz"] += 1 
            else:
                 confidence["waiting_to_buzz(good)"] += 1

data_df = pd.DataFrame({
      'question': questions,
      'correct_answer': correct_answer,
      'guess': guesses,
      'buzz': buzz
})

buzzer_df = qb.buzzer.df
print(buzzer_df)

merged_df = pd.merge(data_df, buzzer_df, on='question')

#merged_df.to_csv('output_data_with_features_0_csv')



correct_acc = correct/(len(answers))          
print("correct: " + str(correct_acc))

confidence_sum = sum(confidence[x] for x in confidence)
print(f'\n-----buzz confidence-----')
print(f'best: {confidence["best(good)"]} ({confidence["best(good)"]/confidence_sum})')
print(f'waiting: {confidence["waiting_to_buzz(good)"]} ({confidence["waiting_to_buzz(good)"]/confidence_sum})')

print(f'\nagressive: {confidence["aggressive_buzz"]} ({confidence["aggressive_buzz"]/confidence_sum})')
print(f'timid: {confidence["scared_to_buzz"]} ({confidence["scared_to_buzz"]/confidence_sum})')

print(f'\n\nBuzz Ratio: {confidence["best(good)"] - confidence["aggressive_buzz"] * 0.5}')

