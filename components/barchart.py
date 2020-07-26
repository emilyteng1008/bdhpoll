import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from poll import Poll, Question


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def getBarChart(pair, dataFrameDict):
    df = dataFrameDict[pair]
    traces = map(
        lambda choice: go.Bar(x=df.index, y=df[choice], name=str(choice)),
        list(df.columns),
    )
    print(df.name)
    dfTranspose = df.transpose()
    tracesTranspose = map(
        lambda choice: go.Bar(
            x=dfTranspose.index, y=dfTranspose[choice], name=str(choice)
        ),
        list(dfTranspose.columns),
    )
    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Graph(
                        id=df.name,
                        figure={
                            "data": list(traces),
                            "layout": {
                                "font": {"size": 35, "family": "Arial"},
                                "title": df.name,
                                "barmode": "stack",
                                "height": 1400,
                                "width": 1400,
                                "titlefont": {"size": 50},
                                "margin": {"b": 250},
                            },
                        },
                    )
                ],
                style={"flex": "50%"},
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id=df.nameTranspose,
                        figure={
                            "data": list(tracesTranspose),
                            "layout": {
                                "font": {"size": 35, "family": "Arial"},
                                "title": df.nameTranspose,
                                "barmode": "stack",
                                "height": 1400,
                                "width": 1400,
                                "titlefont": {"size": 50},
                                "margin": {"b": 250},
                            },
                        },
                    )
                ],
                style={"flex": "50%"},
            ),
        ],
        style={"display": "flex"},
    )


test = Poll("data/questions.csv", "data/data.csv")


app.layout = getBarChart((10, 20), test.getDataFrames())

if __name__ == "__main__":
    app.run_server(debug=True)

