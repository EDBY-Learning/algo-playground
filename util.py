import pandas as pd
import random 
import base64

"""
C 1
C 1
C 2
CI 1
CI 1
CI 2
CIP 1
CIP 1
CIP 2
CIP 2
"""

class StudentQuizDetail:
    def __init__(self):
        self.Type= None
        self.Level= None
        self.Correct= None
        self.Questions= []
    
    def update_current_question(self,current_question):
        if current_question!=None:
            self.Type = current_question['Type']
            self.Level = current_question['Level']
            self.Questions.append({
                'Type':self.Type,
                'Level':self.Level,
                'Correct':"NA",
                'Correct_option':current_question['Answer'],
                'user_answer':"NA"
            })
    
    def update_answer(self,answer):
        if self.Questions[-1]['Correct_option'] ==  answer:
            self.Questions[-1]['Correct'] = True 
        else:
            self.Questions[-1]['Correct'] = False 
        self.Questions[-1]['user_answer'] = answer



def filter_ques(questions,type_=None,level=None):
    if (type_== None) and (level == None):
        return questions
    filtered = questions 
    if type_:
        filtered = list(filter(lambda x: x['Type'] == type_, filtered))
    if level:
        filtered = list(filter(lambda x: x['Level'] == level, filtered))
    if filtered:
        return filtered
    else:
        return questions

class QuizHandler:
    def __init__(self,quiz_details):
        self.class_ = quiz_details['class']
        self.chapter = quiz_details['chapter']
        self.questions = pd.read_csv(quiz_details['filename'],delimiter="|").to_dict('records')
    
    def getNextTypeLevel(self,Type,Level,Jump):
        level_order = [('C',1),('C',2),('CI',1),('C',3),('CI',2),('CIP',1),('CI',3),('CIP',2),('CIP',3)]
        curr_index = level_order.index((Type,Level))

        return level_order[max(min((curr_index+Jump),len(level_order)),0)]

    def question(self,student_quiz_detail):
        if student_quiz_detail.Type == None:
            return filter_ques(self.questions,'C',2)[0]
        else:
            if(student_quiz_detail.Questions[-1]['Correct']):
                if(len(student_quiz_detail.Questions)>1 and student_quiz_detail.Questions[-2]['Correct']):
                    next_question_Type, next_question_Level = self.getNextTypeLevel(student_quiz_detail.Type, student_quiz_detail.Level,2)
                    return filter_ques(self.questions,next_question_Type, next_question_Level)[0]        
                else:            
                    next_question_Type, next_question_Level = self.getNextTypeLevel(student_quiz_detail.Type, student_quiz_detail.Level,1)
                    return filter_ques(self.questions,next_question_Type, next_question_Level)[0]
            else:
                next_question_Type, next_question_Level = self.getNextTypeLevel(student_quiz_detail.Type, student_quiz_detail.Level,-1)
                return filter_ques(self.questions,next_question_Type, next_question_Level)[0]
        # elif student_quiz_detail.Type == 'C':
        #     return filter_ques(self.questions,'CI',1)[0]
        # elif student_quiz_detail.Type == 'CI':
        #     return filter_ques(self.questions,'CIP',2)[0]
        # elif student_quiz_detail.Type == 'CIP':
        #     return filter_ques(self.questions,'C',1)[0]
    
    def analysis(self,student_quiz_detail):
        pass
    
    def check_termination(self):
        pass 
