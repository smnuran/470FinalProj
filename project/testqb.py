from qbmodel import QuizBowlModel
import json 

qb = QuizBowlModel()

question = '''An object orbiting this planet contains sections named Liberty, Equality, and Fraternity.
 A small group of clouds on this planet was nicknamed \"the Scooter\" for its high speed. 
 Volcanoes that eject ice were first observed on an object that orbits this planet.
 The first high resolution images of this object were taken by Voyager 2 and revealed a storm system known as the \"Great Dark Spot\".
 Johann Galle first observed this planet from a telescope using predictions made by Urbain Le Verrier [\"ur-BAIN le vay-ree-AY\"] about its effects on the orbit of Uranus.
 For 10 points, name this dark blue gas giant, the outermost planet in the Solar System.
'''


#can split question into chunks to see how guesser works on harder difficulty. 
splits = question.split(".")

data_source = 'resources/small.guesstrain.json'
with open(data_source) as f:
            doc = json.load(f)
questions_json = doc['questions']
questions = []
answers = []
limit = 200000 #only test this many or less questions 
for question_json in questions_json:
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

for idx, (result_answer, result_bool) in enumerate(result): 
        if answers[idx] == result_answer:
            correct += 1 
            #print("correct | question: " + questions[idx] + " | answer: " + result_answer)
        elif answers[idx].find(result_answer) != -1:
            print("almost | correct answer: " + answers[idx] + " | result: " + result_answer)
            almost_correct += 1


correct_acc = correct/(len(answers))    
almost_acc = (correct+almost_correct)/(len(answers))       
print("correct: " + str(correct_acc))
print("almost_correct: " + str(almost_acc))