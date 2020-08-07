# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from components.poll import Poll
from components.barchart import getBarChart
from components.heatmap import getPValueMatrix
from components.datatable import getDataTable
from components.piechart import getPieChart

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

""" test1 = {(0, 0): 0.5, (0, 1): 0.04, (0, 2): 0.8, (1, 1): 0.6, (1, 2): 0.4, (2, 2): 1}

test = {
    0: Question(["True", "Gender", "Gender", "Male", "Female", "Other"]),
    1: Question(["True", "Race", "What is you Race", "White", "Black", "Asian"]),
    2: Question(["True", "Dating App", "What is you Race", "White", "Black", "Asian"]),
} """
test = Poll("data/questions.csv", "data/data.csv")

app.layout = html.Div(
    children=[
        html.Div(
            html.H1("Spring 2020 Brown Daily Herald Poll "), className="titleLayout"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        getPValueMatrix(test.getPValues(), test.getQuestionDictionary())
                    ],
                    style={"flex": "50%"},
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[getBarChart((10, 17), test.getDataFrames())],
                        ),
                        html.Div(
                            children=[getPieChart((10, 17), test.getDataFrames())],
                            style={"margin-top": "-150px"},
                        ),
                        html.Div(
                            children=[getDataTable((10, 17), test.getDataFrames())],
                        ),
                    ],
                    style={"flex": "50%"},
                ),
            ],
            className="firstRowLayout",
        ),
    ],
    className="pageLayout",
)


if __name__ == "__main__":
    app.run_server(debug=True)

