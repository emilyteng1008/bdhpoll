import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


def getBarChart(pair, dataFrameDict):
    """
    returns an html div with pair of bar charts 
    
    Paramters 
    ---------
    pair: a tuple of ints(pair of question ids)
    dataFrameDict: a dictionary where keys are pairs of question ids, and values are dataframes
    """
    df = dataFrameDict[pair]
    traces = map(
        lambda choice: go.Bar(x=df.index, y=df[choice], name=str(choice)),
        list(df.columns),
    )
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
                                "font": {"size": 15, "family": "Arial"},
                                "title": df.name,
                                "barmode": "stack",
                                "height": 800,
                                "width": "50%",
                                "titlefont": {"size": 25},
                                "margin": {"b": 250},
                                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                                "legend": {"size": "10"},
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
                                "font": {"size": 15, "family": "Arial"},
                                "title": df.nameTranspose,
                                "barmode": "stack",
                                "height": 800,
                                "width": "50%",
                                "titlefont": {"size": 25},
                                "margin": {"b": 250},
                                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                                "legend": {"size": "10"},
                            },
                        },
                    )
                ],
                style={"flex": "50%"},
            ),
        ],
        style={"display": "flex"},
    )

