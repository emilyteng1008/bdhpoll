import numpy as np
import pandas as pd
import scipy.stats as stats
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
        """ self.questionDictionary = self.parseQuestions(questionPath) """
        self.questionPath = questionPath
        self.dataPath = dataPath
        self.questionDictionary = self.getQuestionDictionary()
        self.dataDictionary = self.getDataDictionary()

    def getQuestionDictionary(self):
        """
        returns a dictionary with all the poll questions parsed 

        set i = -1  and if i != 1 to skip the first row of the csv file
        """
        temp = {}
        with open(self.questionPath) as f:
            QUESTION_FILE = csv.reader(f)
            i = -1
            for row in QUESTION_FILE:
                if i != -1:
                    temp[i] = Question(row)
                i += 1
        return temp

    def getDataDictionary(self):
        """
        returns a dictionary with all the responses parsed

        """
        # create an empty dictionary, with key as a pair of index (counting from 0) that represent pair of question
        # with value as an empty array with dimensions of no. of choices in the question
        temp = {}
        for k1, v1 in self.questionDictionary.items():
            for k2, v2 in self.questionDictionary.items():
                if k2 >= k1:
                    temp[(k1, k2)] = np.zeros((len(v1.choices), len(v2.choices)))

        with open(self.dataPath) as f:
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
                                # split multiple choice responses into an array of strings and strip white spaces
                                parsedResponse1 = list(
                                    map(lambda x: x.strip(), rawResponse1.split(","))
                                )
                            else:
                                parsedResponse1 = [rawResponse1]
                            if self.questionDictionary[j].choose_multiple:
                                parsedResponse2 = list(
                                    map(lambda x: x.strip(), rawResponse2.split(","))
                                )
                            else:
                                parsedResponse2 = [rawResponse2]
                            # find the index of responses according to index of choices in self.questionDictionary

                            for choice1 in parsedResponse1:
                                for choice2 in parsedResponse2:
                                    index1 = self.questionDictionary[i].choices[choice1]
                                    index2 = self.questionDictionary[j].choices[choice2]
                                    temp[(i, j)][index1][index2] += 1
        return temp

    def chiSquare(self, pair):
        observed = self.dataDictionary[pair]
        expected = np.zeros(observed.shape)
        for i in range(observed.shape[0]):
            for j in range(observed.shape[1]):
                expected[i][j] = observed[i, :].sum() * observed[:, j].sum()
        expected = expected / (observed.sum())
        chiSquare = (((observed - expected) ** 2) / expected).sum()
        pValue = 1 - stats.chi2.cdf(
            x=chiSquare, df=(observed.shape[0] - 1) * (observed.shape[1] - 1)
        )
        return pValue

    def getPValues(self):
        pValueDictionary = {k: self.chiSquare(k) for k in self.dataDictionary.keys()}
        return pValueDictionary

    def getDataFrames(self):
        df = {k: pd.DataFrame(v) for k, v in self.dataDictionary.items()}
        for k, v in df.items():
            xLabel = [None] * len(self.questionDictionary[k[1]].choices)
            yLabel = [None] * len(self.questionDictionary[k[0]].choices)
            for choice, index in self.questionDictionary[k[1]].choices.items():
                xLabel[index] = choice
            for choice, index in self.questionDictionary[k[0]].choices.items():
                yLabel[index] = choice
            v.columns = xLabel
            v.index = yLabel
            v.name = (
                self.questionDictionary[k[0]].title
                + " vs "
                + self.questionDictionary[k[1]].title
            )
            v.nameTranspose = (
                self.questionDictionary[k[1]].title
                + " vs "
                + self.questionDictionary[k[0]].title
            )
        return df

