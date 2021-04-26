from flask import Flask, render_template, request
import random, copy
from util import QuizHandler, StudentQuizDetail
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

@app.route('/')
def start():
    return '<h1>Quiz </h1>  <form action="/next_question"> <input type="submit" value="start" > </form>'

def process_base64(string):
    if string=='' or pd.isnull(string):
        return 'kk'
    image = (string[2:-1])
    return image

# @app.route('/quiz')
# def quiz():
#     question = quiz_handler.question(student_quiz_detail)
#     update_student_quiz_detail(question)
#     if question=={}:
#         return start() 
#     image = process_base64(question['Encoded_img'])

#     return render_template('main.html', q = question,student_quiz_detail=student_quiz_detail['Questions'],myimage=image)

def get_user_answer(form):
    keys = list(form.keys())
    if len(keys)==1:
        return list(form.keys())[0]
    return None

student_quiz_detail = StudentQuizDetail()

@app.route('/next_question',methods=["GET","POST"])
def next_question():
    if request.method=='GET':
        question = quiz_handler.question(student_quiz_detail)
        
        student_quiz_detail.update_current_question(question)
        image = process_base64(question['Encoded_img'])
        return render_template('main.html',student_quiz_detail=student_quiz_detail.Questions, q = question,myimage=image)

    user_answer = get_user_answer(request.form)
    student_quiz_detail.update_answer(user_answer)

    question = quiz_handler.question(student_quiz_detail)
    student_quiz_detail.update_current_question(question)
    if question=={}:
        return start() 
    image = process_base64(question['Encoded_img'])
    return render_template('main.html',student_quiz_detail=student_quiz_detail.Questions, q = question,myimage=image)

# @app.route('/question_submit',methods=["POST"])
# def quiz(request):
#     print(request.form)
#     next_question()


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