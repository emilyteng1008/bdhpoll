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

test = Poll("data/questions.csv", "data/data.csv")


def getPieChart(pair, dataFrameDict):
    df = dataFrameDict[pair]
    df.loc[:, "Total"] = df.sum(axis=1)
    df.loc["Total", :] = df.sum(axis=0, numeric_only=True)
    df = df.reset_index().rename(columns={"index": ""}, index={"": "Total"})
    values = list(df.loc[:, "Total"])
    labels = list(df.columns)
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels[1:-1],
                values=values,
                textinfo="label+percent",
                insidetextorientation="radial",
            ),
        ]
    )
    return dcc.Graph(figure=fig)


app.layout = getPieChart((0, 0), test.getDataFrames())

if __name__ == "__main__":
    app.run_server(debug=True)
