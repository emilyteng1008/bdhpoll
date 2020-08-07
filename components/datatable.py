import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


def getDataTable(pair, dataFrameDict):
    df = dataFrameDict[pair]
    df.loc[:, "Total"] = df.sum(axis=1)
    df.loc["Total", :] = df.sum(axis=0, numeric_only=True)
    df = df.reset_index().rename(columns={"index": ""}, index={"": "Total"})
    dfTranspose = df.transpose()

    return html.Div(
        children=[
            dash_table.DataTable(
                id="table",
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                style_table={"width": "100%", "height": "300px", "overflowY": "auto",},
                style_header={
                    "backgroundColor": "rgba(0, 0, 0, 0)",
                    "fontWeight": "bold",
                    "whiteSpace": "normal",
                    "height": "auto",
                },
                style_cell={
                    "backgroundColor": "rgba(0, 0, 0, 0)",
                    "padding": "5px",
                    "textAlign": "center",
                },
            )
        ]
    )

