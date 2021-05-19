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



def filter_ques(lo_count_dict, student_quiz_detail, questions,type_=None,level=None, positiveFlag=True):
    if (type_== None) and (level == None):
        return questions
    #base termination cases
    print(lo_count_dict)
    if len(student_quiz_detail.Questions)>MAX_QUESTION_ALLOWED:
        print("here",1)
        return []

    #termination based on question attempted
    if len(student_quiz_detail.Questions)>MIN_QUESTION_TERMINATE:
        print("here",1)
        C_qs = sum([lo_count_dict.get(("C",l),0) for l in range(1,4)])
        CI_qs = sum([lo_count_dict.get(("CI",l),0) for l in range(1,4)])
        CIP_qs = sum([lo_count_dict.get(("CIP",l),0) for l in range(1,4)])
        if CIP_qs>2:
            return []
        if CI_qs>3 and CIP_qs>1:
            return []
        if C_qs>5:
            return []

    filtered = questions
    usedIDList = [elem['ID'] for elem in student_quiz_detail.Questions] 
    
    filtered = [elem for elem in filtered if elem['ID'] not in usedIDList]

    #if no question left
    if not filtered:
        return []
    if type_:
        filtered = list(filter(lambda x: x['Type'] == type_, filtered))
    if level:
        filtered = list(filter(lambda x: x['Level'] == level, filtered))
    if filtered:
        if lo_count_dict[(type_,level)]<ESCAPE:
            print("here i am")
            lo_count_dict[(type_,level)] += 1
            print(lo_count_dict," in same scope")
            return filtered
        
    # else:
    #     return questions
    if lo_count_dict[(type_,level)]>=ESCAPE:
        print("here",3)
        positiveFlag = True
        next_question_Type = {"C":"CI","CI":"CIP","CIP":"CIP"}[type_]
        next_question_Level = 1
        lo_count_dict[(type_,level)] = 0
    else:
        jump = 1 if positiveFlag else -1
        if (type_,level) in [("C",1),("C",2)]: #reflect to ceiling
            positiveFlag = True
            jump = 1

        next_question_Type, next_question_Level = getNextTypeLevel(type_,level,jump)

    filtered = filter_ques(lo_count_dict, student_quiz_detail, questions,next_question_Type,next_question_Level, positiveFlag)
    return filtered

def getNextTypeLevel(level_order,Type,Level,Jump):
    #level_order = [('C',1),('C',2),('CI',1),('C',3),('CI',2),('CIP',1),('CI',3),('CIP',2),('CIP',3)]
    curr_index = level_order.index((Type,Level))
    print("curr_index",curr_index)
    return level_order[max(min((curr_index+Jump),len(level_order)-1),0)]

class QuizHandler:
    def __init__(self,quiz_details):
        self.class_ = quiz_details['class']
        self.chapter = quiz_details['chapter']
        self.questions = pd.read_csv(quiz_details['filename'],delimiter="|").to_dict('records')
        print(pd.Series([(question['Type'],question['Level']) for question in self.questions]).value_counts())
        self.HIGH_JUMP = 2 if len(self.questions)>20 else 1
        self.LOW_JUMP = 1
        self.MAX_QUESTION_ALLOWED = 12 if len(self.questions)>20 else 8
        self.ESCAPE = 2
        self.MIN_QUESTION_TERMINATE = 8 if len(self.questions)>20 else 6

        #create level order
        level_order = list( set( ((question['Type'],question['Level']) for question in self.questions) ))
        self.level_order = sorted(level_order,key=lambda x: 10*(len(x[0])+x[1])+len(x[0]))
        
        self.lo_count_dict =  dict(zip(self.level_order,[0]*len(self.level_order)) )
        print(self.level_order)
        print(self.lo_count_dict)
        
    # def getNextTypeLevel(self,Type,Level,Jump):
    #     level_order = [('C',1),('C',2),('CI',1),('C',3),('CI',2),('CIP',1),('CI',3),('CIP',2),('CIP',3)]
    #     curr_index = level_order.index((Type,Level))

    #     return level_order[max(min((curr_index+Jump),len(level_order)),0)]

    def question(self,student_quiz_detail):
        usedIDList = [elem['ID'] for elem in student_quiz_detail.Questions]
        #use these vars for better probablitic choice
        all_correct = 0
        all_incorrect = 0
        consecutive_correct = 0
        consecutive_incorrect = 0
    
        if student_quiz_detail.Type == None:
            filtered_questions = self.filter_ques(student_quiz_detail, self.questions,'C',1,True)
        else:
            positiveFlag = True
            if(student_quiz_detail.Questions[-1]['Correct']):
                if(len(student_quiz_detail.Questions)>1 and student_quiz_detail.Questions[-2]['Correct']):
                    jump = self.HIGH_JUMP if random.random()<0.7 else self.HIGH_JUMP-1
                    next_question_Type, next_question_Level = getNextTypeLevel(self.level_order,student_quiz_detail.Type, student_quiz_detail.Level,jump)
                    print("xxx:",next_question_Type, next_question_Level)
                else:
                    jump = self.LOW_JUMP if random.random()<0.7 else self.LOW_JUMP-1            
                    next_question_Type, next_question_Level = getNextTypeLevel(self.level_order,student_quiz_detail.Type, student_quiz_detail.Level,jump)
            else:
                positiveFlag = False
                next_question_Type, next_question_Level = getNextTypeLevel(self.level_order,student_quiz_detail.Type, student_quiz_detail.Level,-1)

            filtered_questions = self.filter_ques(student_quiz_detail, self.questions,next_question_Type,next_question_Level,positiveFlag)
            
        if not filtered_questions:
            return None
        return  random.choice(filtered_questions)
    def filter_ques(self, student_quiz_detail, questions,type_=None,level=None, positiveFlag=True):
        if (type_== None) and (level == None):
            return questions
        #base termination cases
        print(self.lo_count_dict)
        if len(student_quiz_detail.Questions)>self.MAX_QUESTION_ALLOWED:
            print("here",1)
            return []

        #termination based on question attempted
        if len(student_quiz_detail.Questions)>self.MIN_QUESTION_TERMINATE:
            print("here",1)
            C_qs = sum([self.lo_count_dict.get(("C",l),0) for l in range(1,4)])
            CI_qs = sum([self.lo_count_dict.get(("CI",l),0) for l in range(1,4)])
            CIP_qs = sum([self.lo_count_dict.get(("CIP",l),0) for l in range(1,4)])
            if CIP_qs>2:
                return []
            if CI_qs>3 and CIP_qs>1:
                return []
            if C_qs>5:
                return []

        filtered = questions
        usedIDList = [elem['ID'] for elem in student_quiz_detail.Questions] 
        
        filtered = [elem for elem in filtered if elem['ID'] not in usedIDList]

        #if no question left
        if not filtered:
            return []
        if type_:
            filtered = list(filter(lambda x: x['Type'] == type_, filtered))
        if level:
            filtered = list(filter(lambda x: x['Level'] == level, filtered))
        if filtered:
            if self.lo_count_dict[(type_,level)]<=self.ESCAPE:
                print("here i am")
                self.lo_count_dict[(type_,level)] += 1
                print(self.lo_count_dict," in same scope")
                return filtered
            
        # else:
        #     return questions
        if self.lo_count_dict[(type_,level)]>self.ESCAPE:
            print("here",3)
            positiveFlag = True
            next_question_Type = {"C":"CI","CI":"CIP","CIP":"CIP"}[type_]
            next_question_Level = 1
            self.lo_count_dict[(type_,level)] = 0
        else:
            jump = 1 if positiveFlag else -1
            if (type_,level) in [("C",1),("C",2)]: #reflect to ceiling
                positiveFlag = True
                jump = 1

            next_question_Type, next_question_Level = getNextTypeLevel(self.level_order,type_,level,jump)

        filtered = self.filter_ques( student_quiz_detail, questions,next_question_Type,next_question_Level, positiveFlag)
        return filtered
    
    def analysis(self,student_quiz_detail):
        pass
    
    def check_termination(self):
        pass 
