# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from heatmap import heatmapLayout
from heatmap import colorMatrix


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


test = {(0, 0): 0.5, (0, 1): 0.04, (0, 2): 0.8, (1, 1): 0.6, (1, 2): 0.4, (2, 2): 1}

app.layout = heatmapLayout(["hello", "yo", "yo"], colorMatrix(test),)


if __name__ == "__main__":
    app.run_server(debug=True)

