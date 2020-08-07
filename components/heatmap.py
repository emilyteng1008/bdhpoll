import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


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
