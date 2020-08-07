import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from poll import Poll, Question

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def setColor(pValue):
    """
    returns a string that is a color of blue 
    smaller the pValue, darker the shade of blue

    Parameters
    ----------
    pValue: a float 
    """
    if pValue <= 0.05:
        return "#0066FF"
    if pValue <= 0.2:
        return "#0099FF"
    if pValue <= 0.5:
        return "lightblue"
    else:
        return "white"


def colorMatrix(pValueDict):
    """
    returns a dictionary where the keys are tuples of numbers (index of question) and values are string (color)
    Parameters
    ---------
    pValueDict: a dictionary where they keys are tuples of numbers(index of question) and values are floats(pValue)
    """
    colorDict = {k: setColor(v) for k, v in pValueDict.items()}
    dim = 0
    for k in colorDict.keys():
        if k[0] > dim:
            dim = k[0]
    temp = np.empty((dim + 1, dim + 1), dtype=object)
    temp.fill("#E0E0E0")
    for k, v in colorDict.items():
        temp[k[0]][k[1]] = v
    return temp


def setLabels(questionsDict):
    labels = [None] * len(questionsDict)
    for k, v in questionsDict.items():
        labels[k] = v.title
    return labels


def bBox(color):
    """
    returns a box in html that has the input color 
    """
    return html.Div(className="coloredbox", style={"background-color": color})


def boxRow(color):
    """
    returns a row of boxes in html

    Parameter
    ---------
    color: array of strings 
    """
    return html.Div(children=list(map(bBox, color)), className="boxRow",)


def boxBox(color):
    """
    return a box of the input color

    Parameter
    ---------
    color: string
    """
    return html.Div(children=list(map(boxRow, color)))


def labelX(name):
    """
    returns a x label in html 
    
    Parameter
    ---------
    name: string
    """

    return html.Div(
        html.P(children=name, className="labelX-text"), className="labelX-div"
    )


def labelY(name):
    """
    returns a y label in html 
    
    Parameter
    ---------
    name: string 
    """
    return html.Div(
        html.P(children=name, className="labelY-text"), className="labelY-div"
    )


def labelColumn(labels):
    """
    returns a column of y labels in html

    Parameter
    ---------
    labels: an array of strings
    """
    return html.Div(list(map(labelY, labels)), className="labels-format")


def labelRow(labels):
    """
    returms a row of x labels in html

    Parameter
    --------
    labels: an array of strings
    """
    return html.Div(list(map(labelX, labels)), className="labels-format")


def heatmapLayout(labels, colors):
    """
    returns a heatmap with xlabels and ylabels in html

    Paramter
    ---------
    labels: an array of strings 
    colors: an array of strings
    """
    return html.Div(
        children=[
            html.Div(labelColumn(labels), className="layout-labelsCol"),
            html.Div(
                children=[labelRow(labels), boxBox(colors),],
                className="layout-labelsRowHeatmap",
            ),
        ],
        className="layout-heatmap",
    )


def getPValueMatrix(pValueDict, questionDict):
    pValues = np.full((len(pValueDict), len(pValueDict)), np.nan)
    Label = [None] * len(questionDict)
    for k, v in questionDict.items():
        Label[k] = v.title
    for k, v in pValueDict.items():
        pValues[k[0]][k[1]] = v
    fig = go.Figure(data=go.Heatmap(z=pValues, x=Label, y=Label))
    fig.update_layout(
        height=1450,
        width=1300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return html.Div(children=[dcc.Graph(figure=fig)])


test = Poll("data/questions.csv", "data/data.csv")

app.layout = getPValueMatrix(test.getPValues(), test.getQuestionDictionary())

if __name__ == "__main__":
    app.run_server(debug=True)
