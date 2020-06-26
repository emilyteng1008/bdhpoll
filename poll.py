import numpy as np
from scipy.stats import chisquare
import csv 

class Question: 
    def __init__(self, row): 
        self.title = row[1] # the generic name for ea. question
        self.text = row[2] # the actual text of ea. question
        self.choices = {} 
        for i in range(3, len(row)):
            if row[i] == "": 
                break
            else: 
                self.choices[row[i]] = i - 3

""" test_row = [True, "Gender", "Gender", "Male", "Female", "Other"]
test = Question(test_row)
print test.choices
print test.title
print test.text """




class Poll: 
    def __init__(self, questionPath): 
        self.questionDictionary = self.parseQuestions(questionPath)
        """ self.data = self.parseD(data) """
    def parseQuestions(self, questionsCSV): 
        temp = {}
        with open(questionsCSV) as f: 
            QUESTION_FILE = csv.reader(f)
            i = -1
            for row in QUESTION_FILE: 
                if i != -1: 
                    temp[i] = Question(row)
                i += 1
        return temp

        
""" test = Poll('questions.csv')
for k, v in test.questionDictionary.items():
    print(v.choices) """