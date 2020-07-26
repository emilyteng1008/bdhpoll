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
    values1 = list(df.iloc[-1])
    labels1 = list(df.columns)
    print(values1)
    print(df)
    fig1 = go.Figure(
        data=[
            go.Pie(
                labels=labels1[1:-1],
                values=values1[1:-1],
                textinfo="label+percent",
                insidetextorientation="radial",
            ),
        ]
    )

    values2 = list(df["Total"])
    labels2 = list(df.iloc[:, 0])
    print(labels2)
    print(values2)
    fig2 = go.Figure(
        data=[
            go.Pie(
                labels=labels2,
                values=values2[:-1],
                textinfo="label+percent",
                insidetextorientation="radial",
            ),
        ]
    )
    fig1.update_layout(showlegend=False)
    fig2.update_layout(showlegend=False)
    return html.Div(
        children=[
            html.Div(children=[dcc.Graph(figure=fig1)]),
            html.Div(children=[dcc.Graph(figure=fig2)]),
        ],
    )


app.layout = getPieChart((0, 10), test.getDataFrames())

if __name__ == "__main__":
    app.run_server(debug=True)
