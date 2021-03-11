import pandas as pd
import random 
import base64
class QuizzHandler:
    def __init__(self,quizz_details,last_quzz_detail, prereq_score):
        self.quizz_file = quizz_details['filename']
        self.topic = quizz_details['topic']
        self.last_quzz_detail = last_quzz_detail
        self.prereq_score = prereq_score
        self.question_count = 0
    
    def load_quizz(self):
        self.all_qs = pd.read_csv(self.quizz_file, sep="|")
        self.all_quizz_qs = self.all_qs[self.all_qs['Topic ']==self.topic]
        self.cs = self.all_quizz_qs[self.all_quizz_qs['Type']=='C']
        self.cis = self.all_quizz_qs[self.all_quizz_qs['Type']=='CI']
        self.cips = self.all_quizz_qs[self.all_quizz_qs['Type']=='CIP']

        print(self.all_qs.columns)




    
    def question(self):
        if self.check_termination():
            return {}
        index = random.randint(0,len(self.all_qs)-1)
        question = self.all_qs.iloc[index].to_dict()
        self.question_count+=1
        return question
    
    def check_termination(self):
        if self.question_count>12:
            self.question_count=0
            return True
        pass


    
    
