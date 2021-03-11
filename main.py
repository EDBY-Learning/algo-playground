from flask import Flask, render_template, request
import random, copy
from util import QuizzHandler
import pandas as pd

app = Flask(__name__)

original_questions = {
 #Format is 'question':[options]
 'Taj Mahal':['Agra','New Delhi','Mumbai','Chennai'],
 'Great Wall of China':['China','Beijing','Shanghai','Tianjin'],
 'Petra':['Ma\'an Governorate','Amman','Zarqa','Jerash'],
 'Machu Picchu':['Cuzco Region','Lima','Piura','Tacna'],
 'Egypt Pyramids':['Giza','Suez','Luxor','Tanta'],
 'Colosseum':['Rome','Milan','Bari','Bologna'],
 'Christ the Redeemer':['Rio de Janeiro','Natal','Olinda','Betim']
}

questions = copy.deepcopy(original_questions)

last_quzz_detail = {
    "Score":{
        "C":20,
        "CI":30,
        "CIP":40
    }
}

prereq_score = {
    "P1":20
}

quizz_details = {
    "filename": 'E://school//template questions//questionTemplateGenerator//output//CBSE-maths-ch-4.csv',
    "topic":"all"
}
quizz_handler = QuizzHandler(quizz_details, last_quzz_detail, prereq_score)
quizz_handler.load_quizz()


@app.route('/')
def start():
    return '<h1>Quizz </h1>  <form action="/quizz"> <input type="submit" value="start" > </form>'

def process_base64(string):
    if string=='' or pd.isnull(string):
        return 'kk'
    image = (string[2:-1])
    return image

@app.route('/quizz')
def quiz():
 question = quizz_handler.question()
 
 if question=={}:
     return start() 
 image = process_base64(question['Encoded_img'])
 
 return render_template('main.html', q = question,myimage=image)


# @app.route('/quiz', methods=['POST'])
# def quiz_answers():
#  correct = 0
#  for i in questions.keys():
#   answered = request.form[i]
#   if original_questions[i][0] == answered:
#    correct = correct+1
#  return '<h1>Correct Answers: <u>'+str(correct)+'</u></h1>'

if __name__ == '__main__':
 app.run(debug=True)