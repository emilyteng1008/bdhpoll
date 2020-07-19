import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from poll import Question
from poll import Poll

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

test = Poll("questions.csv", "data.csv")


def getDataTable(pair, DataFrameDict):
    df = DataFrameDict[pair]
    df = df.reset_index().rename(columns={"index": " "})
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_table={"width": "50%"},
    )


app.layout = getDataTable((15, 23), test.getDataFrames())


if __name__ == "__main__":
    app.run_server(debug=True)
