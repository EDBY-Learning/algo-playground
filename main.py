from flask import Flask, render_template, request
import random, copy
from util import QuizHandler, StudentQuizDetail
import pandas as pd

app = Flask(__name__)

quiz_details = {
    "filename": './content/class6-ch4.csv',
    "topic":"all",
    "chapter":4,
    "class":6
}



@app.route('/')
def start():
    return '<h1>Quiz </h1>  <form action="/next_question"> <input type="submit" value="start" > </form>'

def process_base64(string):
    if string=='' or pd.isnull(string):
        return 'kk'
    image = (string[2:-1])
    return image

def get_user_answer(form):
    keys = list(form.keys())
    if len(keys)==1:
        return list(form.keys())[0]
    return None

student_quiz_detail = None
quiz_handler = None

@app.route('/next_question',methods=["GET","POST"])
def next_question():
    global quiz_handler
    global student_quiz_detail
    if request.method=='GET':
        quiz_handler = QuizHandler(quiz_details)
        student_quiz_detail = StudentQuizDetail()
        question = quiz_handler.question(student_quiz_detail)
        
        student_quiz_detail.update_current_question(question)
        image = process_base64(question['Encoded_img'])
        return render_template('main.html',student_quiz_detail=student_quiz_detail.Questions, q = question,myimage=image)

    user_answer = get_user_answer(request.form)
    student_quiz_detail.update_answer(user_answer)

    question = quiz_handler.question(student_quiz_detail)
    student_quiz_detail.update_current_question(question)
    if question==None:
        #get_report
        print("QUIZZ ENDED")
        return start() 
    image = process_base64(question['Encoded_img'])
    return render_template('main.html',student_quiz_detail=student_quiz_detail.Questions, q = question,myimage=image)

if __name__ == '__main__':
    app.run(debug=True)