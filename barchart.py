import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from poll import Question
from poll import Poll

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def getBarChart(pair, dataFrameDict):
    df = dataFrameDict[pair]
    traces = map(
        lambda choice: go.Bar(x=df.index, y=df[choice], name=str(choice)),
        list(df.columns),
    )
    barchart = dcc.Graph(
        id=df.name,
        figure={
            "data": list(traces),
            "layout": {
                "title": df.name,
                "barmode": "stack",
                "height": 1400,
                "width": 1400,
                "titlefont": {"size": 50},
                "legendfont": {"size": 35},
            },
        },
    )
    return barchart


test = Poll("questions.csv", "data.csv")

app.layout = html.Div(children=[getBarChart((10, 20), test.getDataFrames())])


if __name__ == "__main__":
    app.run_server(debug=True)

