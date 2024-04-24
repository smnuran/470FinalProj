from qbmodel import QuizBowlModel

qb = QuizBowlModel()

question = '''An object orbiting this planet contains sections named Liberty, Equality, and Fraternity.
 A small group of clouds on this planet was nicknamed \"the Scooter\" for its high speed. 
 Volcanoes that eject ice were first observed on an object that orbits this planet.
 The first high resolution images of this object were taken by Voyager 2 and revealed a storm system known as the \"Great Dark Spot\".
 Johann Galle first observed this planet from a telescope using predictions made by Urbain Le Verrier [\"ur-BAIN le vay-ree-AY\"] about its effects on the orbit of Uranus.
 For 10 points, name this dark blue gas giant, the outermost planet in the Solar System.
'''

result = qb.guess_and_buzz([question])

print(result)