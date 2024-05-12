from qbmodel import QuizBowlModel
import json 
import pandas as pd 



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



qb = QuizBowlModel()

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
limit = 20 #only test this many or less questions 
test_splits = False 
for question_json in questions_json:
      
      if test_splits:
            #if you want to test question splits: 
            splits = get_splits(question_json['text'])
            #print(splits)

            for q in splits:
                  if q is not None and q != "":
                        questions.append(q)
                        answers.append(question_json["answer"])

                        

      question = question_json['text']
      answer = question_json['answer']
      questions.append(question)
      answers.append(answer)

      limit -= 1 
      if limit < 0:
            break 




#questions = # splits #[question]
result = qb.guess_and_buzz(questions)
correct = 0 
almost_correct = 0

guesses = []
buzz = []
correct_answer = []
for idx, (result_answer, result_bool) in enumerate(result): 
        if result_answer is None or answers[idx] is None:
            result_answer = " "
            print(f"abandoned: {result_answer} or {answers[idx]}")
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(False)

        if answers[idx] == result_answer:
            correct += 1 
            guesses.append(result_answer)
            correct_answer.append(result_answer)
            buzz.append(True)
            #print("correct | question: " + questions[idx] + " | answer: " + result_answer)
        elif answers[idx].find(result_answer) != -1:
            #print("almost | correct answer: " + answers[idx] + " | result: " + result_answer)
            almost_correct += 1
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(True)
        elif compare_answers(result_answer, answers[idx]):
            almost_correct += 1
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(True)
        else:
            guesses.append(result_answer)
            correct_answer.append(answers[idx])
            buzz.append(False)

data_df = pd.DataFrame({
      'question': questions,
      'correct_answer': correct_answer,
      'guess': guesses,
      'buzz': buzz
})

#json.dump(data_df)
#data_df.to_csv('output_data_csv')



correct_acc = correct/(len(answers))    
almost_acc = (correct+almost_correct)/(len(answers))       
print("correct: " + str(correct_acc))
print("almost_correct: " + str(almost_acc))


