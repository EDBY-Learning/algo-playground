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
                'ID': current_question['ID'],
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



def filter_ques(questions,type_=None,level=None, positiveFlag=True):
    if (type_== None) and (level == None):
        return questions
    filtered = questions 
    if type_:
        filtered = list(filter(lambda x: x['Type'] == type_, filtered))
    if level:
        filtered = list(filter(lambda x: x['Level'] == level, filtered))
    if filtered:
        return filtered
    # else:
    #     return questions
    else:
        jump = 1 if positiveFlag else -1
        next_question_Type, next_question_Level = getNextTypeLevel(type_,level,jump)
        filtered = filter_ques(questions,next_question_Type,next_question_Level, positiveFlag)
    return filtered

def getNextTypeLevel(Type,Level,Jump):
    level_order = [('C',1),('C',2),('CI',1),('C',3),('CI',2),('CIP',1),('CI',3),('CIP',2),('CIP',3)]
    curr_index = level_order.index((Type,Level))
    print("curr_index",curr_index)
    return level_order[max(min((curr_index+Jump),len(level_order)-1),0)]

class QuizHandler:
    def __init__(self,quiz_details):
        self.class_ = quiz_details['class']
        self.chapter = quiz_details['chapter']
        self.questions = pd.read_csv(quiz_details['filename'],delimiter="|").to_dict('records')
    
    # def getNextTypeLevel(self,Type,Level,Jump):
    #     level_order = [('C',1),('C',2),('CI',1),('C',3),('CI',2),('CIP',1),('CI',3),('CIP',2),('CIP',3)]
    #     curr_index = level_order.index((Type,Level))

    #     return level_order[max(min((curr_index+Jump),len(level_order)),0)]

    def question(self,student_quiz_detail):
        usedIDList = [elem['ID'] for elem in student_quiz_detail.Questions]
        if student_quiz_detail.Type == None:
            return filter_ques(self.questions,'C',1,True)[0]
        else:
            positiveFlag = True
            if(student_quiz_detail.Questions[-1]['Correct']):
                if(len(student_quiz_detail.Questions)>1 and student_quiz_detail.Questions[-2]['Correct']):
                    next_question_Type, next_question_Level = getNextTypeLevel(student_quiz_detail.Type, student_quiz_detail.Level,2)
                    print("xxx:",next_question_Type, next_question_Level)
                else:            
                    next_question_Type, next_question_Level = getNextTypeLevel(student_quiz_detail.Type, student_quiz_detail.Level,1)
            else:
                positiveFlag = False
                next_question_Type, next_question_Level = getNextTypeLevel(student_quiz_detail.Type, student_quiz_detail.Level,-1)

            filtered_questions = filter_ques(self.questions,next_question_Type,next_question_Level,positiveFlag)
            # print(next_question_Type,next_question_Level)
            # while(len(filtered_questions)==0):
            #     # jump = 1 if positiveFlag else -1
            #     # print("jump: ",jump)
            #     # print("previous",next_question_Type,next_question_Level)
            #     # next_question_Type, next_question_Level = self.getNextTypeLevel(next_question_Type,next_question_Level,jump)
            #     # filtered_questions = filter_ques(self.questions,next_question_Type,next_question_Level)
            #     # print("next",next_question_Type,next_question_Level)
            #     filtered_questions = filter_ques(self.questions,next_question_Type,next_question_Level,positiveFlag)
            candidateQuestions = [elem for elem in filtered_questions if elem['ID'] not in usedIDList]
            while(len(candidateQuestions)==0):
                jump = 1 if positiveFlag else -1
                next_question_Type, next_question_Level = getNextTypeLevel(next_question_Type,next_question_Level,jump)
                filtered_questions = filter_ques(self.questions,next_question_Type,next_question_Level,positiveFlag)
                candidateQuestions = [elem for elem in filtered_questions if elem['ID'] not in usedIDList]
            return candidateQuestions[0]
            # return [elem for elem in filtered_questions if elem['ID'] not in usedIDList][0]
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
