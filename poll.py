import numpy as np
from scipy.stats import chisquare
import csv


class Question:
    def __init__(self, row):
        self.choose_multiple = True if row[0].upper() == "TRUE" else False
        self.title = row[1]  # the generic name for ea. question
        self.text = row[2]  # the actual text of ea. question
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
    def __init__(self, questionPath, dataPath):
        self.questionDictionary = self.parseQuestions(questionPath)
        self.data = self.parseData(dataPath)

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

    def parseData(self, dataCSV):
        temp = {}
        for k1, v1 in self.questionDictionary.items():
            for k2, v2 in self.questionDictionary.items():
                if k2 >= k1:
                    temp[(k1, k2)] = np.zeros((len(v1.choices), len(v2.choices)))

        with open(dataCSV) as f:
            DATA_FILE = csv.reader(f)
            isQuestion = False
            for row in DATA_FILE:
                if isQuestion == False:
                    isQuestion = True
                    continue
                for i, rawResponse1 in enumerate(row):
                    for j, rawResponse2 in enumerate(row):
                        if j >= i:
                            if self.questionDictionary[i].choose_multiple:
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
print(test.data)

