from flask import Flask, render_template, request
import random, copy
from util import QuizHandler
import pandas as pd

app = Flask(__name__)


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

quiz_details = {
    "filename": './content/class6-ch4.csv',
    "topic":"all",
    "chapter":4,
    "class":6
}

student_quiz_detail = {
    'Type':None,
    'Level':None,
    'Correct':None,
    "Questions":[]
}

quiz_handler = QuizHandler(quiz_details)

def update_student_quiz_detail(question,answer='a'):
    global student_quiz_detail 
    student_quiz_detail['Type'] = question['Type']
    student_quiz_detail['Level'] = question['Level']
    student_quiz_detail['Correct'] = True 
    student_quiz_detail['Questions'].append({
        'Type':student_quiz_detail['Type'],
        'Level':student_quiz_detail['Level'],
        'Correct':student_quiz_detail['Correct']
    })

@app.route('/')
def start():
    return '<h1>Quiz </h1>  <form action="/quiz"> <input type="submit" value="start" > </form>'

def process_base64(string):
    if string=='' or pd.isnull(string):
        return 'kk'
    image = (string[2:-1])
    return image

@app.route('/quiz')
def quiz():
    question = quiz_handler.question(student_quiz_detail)
    update_student_quiz_detail(question)
    if question=={}:
        return start() 
    image = process_base64(question['Encoded_img'])

    return render_template('main.html', q = question,student_quiz_detail=student_quiz_detail['Questions'],myimage=image)


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