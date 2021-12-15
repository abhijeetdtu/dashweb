from dashweb.web.dash.DashApp import DashApp
from dashweb.plotting_constants import THEME , ColorPalette

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from plotnine import *

import logging
import pandas as pd
import numpy as np
import random
import json

logging.basicConfig(level = logging.INFO)

class WordTrend(DashApp):

    def __init__(self,route,flaskApp):
        super().__init__(route,flaskApp)


    def _filteredDf(self):
        df = pd.DataFrame({"x"  :np.random.randint(0,100,100) , "y"  :np.random.randint(0,100,100) , "fill" : np.random.randint(0,3,100)})
        df["fill"] = df["fill"].astype("category")
        return df

    def _chart(self,df):

        if df is None:
            return self.getErrorPlot(self.ERROR_MSG)
        #+ colors \
        p =  ( ggplot(df , aes(x="x" , y="y" , fill="fill" , size=10))
            + geom_point()
            + theme_bw()
            + theme(figure_size=(20,5) , panel_grid_major=element_blank() , panel_grid_minor=element_blank())
            )
        return p


    def setupOptions(self):
        pass

    def makeInputLayout(self):
        return html.Div(className="row" , children=[])

    def setupCallBacks(self):
        pass

    def makeLayout(self):
        self.app.layout = html.Div(className="dash-container container p-0 m-0", children=[
            self.makeInputLayout(),
            dcc.Loading(
                id="loading-holder",
                color=THEME.LOADER_COLOR,
                type=THEME.LOADER_TYPE,
                children=[
                    html.Div(className="row-fluid" , children=[
                        html.Div(id=DashApp.HTML_IDS.IMG,  className="plot-holder-div" , children=[self.plot_html()])
                    ])
                ]
            )
        ])
        self.setupCallBacks()
