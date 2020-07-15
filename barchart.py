import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from poll import Question
from poll import Poll


test_data = {
    (0, 0): [[0, 1, 2], [3, 4, 5], [5, 6, 7]],
    (1, 0): [[1, 1], [2, 2], [3, 3]],
    (1, 1): [[0, 1], [2, 0]],
}


test_question = {
    0: Question(["True", "Race", "Race", "Black", "White", "Other"]),
    1: Question(["True", "Gender", "Gender", "Male", "Female"]),
}


def getDataFrame(dataDict, questionDict):
    df = {k: pd.DataFrame(v) for k, v in dataDict.items()}
    for k, v in df.items():
        xLabel = [None] * len(questionDict[k[0]].choices)
        yLabel = [None] * len(questionDict[k[1]].choices)
        for choice, index in questionDict[k[0]].choices.items():
            xLabel[index] = choice
        for choice, index in questionDict[k[1]].choices.items():
            yLabel[index] = choice
        v.columns = xLabel
        v.index = yLabel
    return df


test_df = getDataFrame(test_data, test_question)
print(test_df[(1, 0)])

