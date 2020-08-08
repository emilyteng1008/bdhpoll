import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


def getPieChart(pair, dataFrameDict):
    """
    returns a html div with pair of piecharts 
    
    Parameters
    ----------
    pair: a tuple of ints (pair of question ids)
    dataFrameDict: a dictionary where keys are tuples (pairs of question ids) and values are dataframes 
    """
    df = dataFrameDict[pair]
    df.loc[:, "Total"] = df.sum(axis=1)
    df.loc["Total", :] = df.sum(axis=0, numeric_only=True)
    df = df.reset_index().rename(columns={"index": ""}, index={"": "Total"})
    values1 = list(df.iloc[-1])
    labels1 = list(df.columns)
    fig1 = go.Figure(data=[go.Pie(labels=labels1[1:-1], values=values1[1:-1],),])
    # transpose the dataframe to get the other pie chart
    values2 = list(df["Total"])
    labels2 = list(df.iloc[:, 0])
    fig2 = go.Figure(data=[go.Pie(labels=labels2, values=values2[:-1],),])
    fig1.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        width=600,
        height=600,
    )
    fig2.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        width=600,
        height=600,
    )
    return html.Div(
        children=[
            html.Div(
                children=[dcc.Graph(figure=fig2)],
                style={
                    "flex": "50%",
                    "width": "50%",
                    "height": "100ox",
                    "margin-right": "20px",
                },
            ),
            html.Div(
                children=[dcc.Graph(figure=fig1)],
                style={"flex": "50%", "width": "50%", "height": "100px"},
            ),
        ],
        style={"display": "flex"},
    )

