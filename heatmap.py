import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np


def setColor(pValue):
    """
    returns a string that is a color of blue 
    smaller the pValue, darker the shade of blue

    Parameters
    ----------
    pValue: a float 
    """
    if pValue <= 0.05:
        return "navy"
    if pValue <= 0.2:
        return "blue"
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
    temp.fill("grey")
    for k, v in colorDict.items():
        temp[k[0]][k[1]] = v
    return temp


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
    
    """
    return html.Div(children=list(map(boxRow, color)))


def labelX(name):
    return html.Div(
        html.P(children=name, className="labelX-text"), className="labelX-div"
    )


def labelY(name):
    return html.Div(
        html.P(children=name, className="labelY-text"), className="labelY-div"
    )


def labelColumn(labels):
    return html.Div(list(map(labelY, labels)), className="labels-format")


def labelRow(labels):
    return html.Div(list(map(labelX, labels)), className="labels-format")


def heatmapLayout(labels, colors):
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

