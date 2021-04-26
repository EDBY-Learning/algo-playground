from flask import Flask, render_template, request
import random, copy
from util import QuizzHandler
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

quizz_details = {
    "filename": r"E:\school\algo_playground_experiments\algo-playground\questions\CBSE-maths-class-6-ch-4.csv",
    "topic":"all"
}
quizz_handler = QuizzHandler(quizz_details, last_quzz_detail, prereq_score)
quizz_handler.load_quizz()
prev_question = None

@app.route('/')
def start():
    return '<h1>Quizz </h1>  <form action="/next_question"> <input type="submit" value="start" > </form>'

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


@app.route('/next_question',methods=["GET","POST"])
def next_question():
    global prev_question
    if request.method=='GET':
        question = quizz_handler.next_question()
        image = process_base64(question['Encoded_img'])
        return render_template('main.html', q = question,myimage=image)

    user_answer = get_user_answer(request.form)
    quizz_handler.submit_answer(user_answer)
    

    question = quizz_handler.next_question()
    if question=={}:
        return start() 
    image = process_base64(question['Encoded_img'])
    return render_template('main.html', q = question,myimage=image)

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