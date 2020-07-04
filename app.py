# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def bBox(color):
    return html.Div(className="coloredbox", style={"background-color": color})


def boxRow(color):
    return html.Div(children=list(map(bBox, color)), className="boxRow",)


def boxBox(color):
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


app.layout = html.Div(
    children=[
        html.Div(
            labelColumn(["hello", "yo", "yo"]),
            style={"float": "left", "background-color": "grey", "margin-top": "30px"},
        ),
        html.Div(
            children=[
                labelRow(["hello", "yo", "yo"]),
                boxBox([["blue", "green", "yellow"], ["blue"]]),
            ],
            style={"float": "left", "background-color": "yellow"},
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)

