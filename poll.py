import numpy as np
from scipy.stats import chisquare
import csv


class Question:
    """ 
    A class that represents a question 

    ...

    Attributes 
    ----------
    choose_multiple : bool
        a boolean that checks whether the question is multiple choice or single choice

    title: str
        the simplified name of the question (e.g., "Gender" is the title for question "What is your gender?" )

    text: str
        the question 

    Choices : dict
        a dictionary that where the key is a string of choice, value is a int of id (that counts from 0)
        (e.g., {"Female" : 0, "Male" : 1, "Other": 2})

    """

    def __init__(self, row):
        """
        Parameters 
        ----------

        row: a array of strings with choose_multiple, title, text, and choices
        """
        self.choose_multiple = True if row[0].upper() == "TRUE" else False
        self.title = row[1]
        self.text = row[2]
        self.choices = {}
        for i in range(3, len(row)):
            if row[i] == "":
                break
            else:
                self.choices[row[i].strip()] = i - 3


""" test_row = ["True", "Gender", "Gender", "Male", "Female", "Other"]
test = Question(test_row)
print(test.choose_multiple)
print(test.choices)
print(test.title)
print(test.text) """


class Poll:
    """
    A class that represents all the questions and data  
    
    ...
    Attributes 
    ----------
    
    questionDictionary : dict
        a dictionary with key that is an int (id that counts from 0) and value that is the class Question
    
    
    data: dict 
        a dictionary with key that is a tuple (a pair of ids that uniquely represent ea. question) 
        value that is an array of arrays (a matrix with x,y label as choices of ea. question)
    """

    def __init__(self, questionPath, dataPath):
        """
        Parameters
        ---------
        questionPath: csv file 
            a file that stores all the poll questions 

        dataPath: csv file 
            a file that stores all the poll responses 
        """
        self.questionDictionary = self.parseQuestions(questionPath)
        self.data = self.parseData(dataPath)

    def parseQuestions(self, questionsCSV):
        """
        returns a dictionary with all the poll questions parsed 

        set i = -1  and if i != 1 to skip the first row of the csv file
        """
        temp = {}
        with open(questionsCSV) as f:
            QUESTION_FILE = csv.reader(f)
            i = -1
            for row in QUESTION_FILE:
                if i != -1:
                    temp[i] = Question(row)
                i += 1
        return temp

    def parseData(self, dataCSV):
        """
        returns a dictionary with all the responses parsed

        """
        temp = {}
        for k1, v1 in self.questionDictionary.items():
            for k2, v2 in self.questionDictionary.items():
                if k2 >= k1:
                    temp[(k1, k2)] = np.zeros((len(v1.choices), len(v2.choices)))

        with open(dataCSV) as f:
            DATA_FILE = csv.reader(f)
            isQuestion = False
            # iterate over ea. row in the file
            for row in DATA_FILE:
                # skip the first row in the file, because the questions start in second row
                if isQuestion == False:
                    isQuestion = True
                    continue
                # iterate over every pair of columns in ea. row
                for i, rawResponse1 in enumerate(row):
                    for j, rawResponse2 in enumerate(row):
                        # avoid repetitive pairs of questions (e.g., "race" and "gender" is the same as "gender" and "race")
                        if j >= i:
                            if self.questionDictionary[i].choose_multiple:
                                # splits multiple choices into an array of strings and strips white spaces
                                parsedResponse1 = map(
                                    lambda x: x.strip(), rawResponse1.split(",")
                                )
                            else:
                                parsedResponse1 = [rawResponse1]
                            if self.questionDictionary[j].choose_multiple:
                                parsedResponse2 = map(
                                    lambda x: x.strip(), rawResponse2.split(",")
                                )
                            else:
                                parsedResponse2 = [rawResponse2]
                            for choice1 in parsedResponse1:
                                for choice2 in parsedResponse2:
                                    index1 = self.questionDictionary[i].choices[choice1]
                                    index2 = self.questionDictionary[j].choices[choice2]
                                    temp[(i, j)][index1][index2] += 1
        return temp


""" test = Poll("testquestions.csv")
for k, v in test.questionDictionary.items():
    print(v.title + str(v.choose_multiple))

test1 = ["FALSE", "Female", "Sophmore", "Yes"]
for i, r in enumerate(test1):
    print(str(i) + r) """

test = Poll("questions.csv", "data.csv")
print(Poll.__doc__)

