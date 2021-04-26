import pandas as pd
import random 
import base64

"""
C 1
C 1
CI 1
C 2
CI 1
CI 2
CIP 1
CIP 1
CIP 2
CIP 2
"""

def filter_ques(questions,type_=None,level=None):
    if (type_== None) and (level == None):
        return questions
    filtered = questions 
    if type_:
        filtered = list(filter(lambda x: x['Type'] == type_, filtered))
    if level:
        filtered = list(filter(lambda x: x['Type'] == type_, filtered))
    if filtered:
        return filtered
    else:
        return questions

class QuizHandler:
    def __init__(self,quiz_details):
        self.class_ = quiz_details['class']
        self.chapter = quiz_details['chapter']
        self.questions = pd.read_csv(quiz_details['filename'],delimiter="|").to_dict('records')
    
    def question(self,student_quiz_detail):
        if student_quiz_detail['Type'] == None:
            return filter_ques(self.questions,'C',2)[0]
        elif student_quiz_detail['Type'] == 'C':
            return filter_ques(self.questions,'CI',1)[0]
        elif student_quiz_detail['Type'] == 'CI':
            return filter_ques(self.questions,'CIP',2)[0]
        elif student_quiz_detail['Type'] == 'CIP':
            return filter_ques(self.questions,'C',1)[0]
        
    
    def check_answer(self,user_answer):
        if self.curr_question['Answer'].lower()==user_answer.lower():
            return True
        return False
    
    def submit_answer(self,user_answer):
        #if skipped i.e. user_answer==None
        if user_answer==None:
            #skipped the question
            pass
        else:
            #check answer and update algorithm
            pass
    
    def get_curr_question(self):
        return self.curr_question
    
    def check_termination(self):
        pass 
