import dash
import base64
from io import BytesIO
import dash_html_components as html
import pathlib
import os
import random

from pandas import DataFrame
from plotnine import ggplot ,aes, geom_label ,geom_text, theme, element_blank , element_text

from multiprocessing.dummy import Pool as ThreadPool

from dashweb.plotting_constants import THEME
from dashweb.utils import getLogging

log = getLogging()

import time



class DashApp:

    class HTML_IDS:
        IMG = "plot"
        WORD_INPUT = 'word_input'
        CHECKLIST = "checklist"

        CHECKLIST_ALL = "All"
        SHADOW_REG_CLS = "shadow p-1 bg-white rounded"
        SHADOW_SM_CLS = "shadow-sm p-1 bg-white rounded"

    def __init__(self, route , flaskApp):
        self.imp_dump = os.path.join(pathlib.Path(__file__).resolve().parent.parent.absolute() , "static" , "temp_imgs")
        self.pool = ThreadPool(5)
        external_stylesheets = [
            'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css'
        ]
        self.app = dash.Dash(__name__,server=flaskApp
                                    , routes_pathname_prefix=route
                                    , external_stylesheets=external_stylesheets)

        self.app.index_string = """
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
                <link rel="stylesheet" href="/static/css/dash.css"/>
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        """

        self.create()

    def getErrorPlot(self , msg="Error Occured"):
        df = DataFrame({"x" : [10] , "y":[2] , "label":[msg]})
        p = ggplot(df , aes(x="x" , y="y" , label="label")) + geom_text(color="white") \
            + THEME.cat_colors_lines \
              + THEME.mt \
              + theme(figure_size=(20,4) ,axis_text=element_blank(), panel_grid_major=element_blank() , panel_grid_minor=element_blank())
        return p

    def plotToImgSrc(self,p):
        log.info("Img To SRC")
        start_time = time.time()
        if type(p) == list:
            plot_img = self.pool.map(lambda pi:self.plotToImgSrc(pi) , p) #[self.plotToImgSrc(pi) for pi in p]
        else:
            fig = p.draw()
            tmpfile = BytesIO()
            fig.savefig(tmpfile, format='png' ,bbox_inches='tight')
            #log.info("Saved--")
            encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
            plot_img = 'data:image/png;base64,{}'.format(encoded)
        log.info(f"Done - Img To SRC - {time.time()-start_time}")
        return plot_img

    def srcToImgs(self,src):
        id = "abc"
        if type(src) != list:
            src = [src]

        imgCls = ""
        return [ html.Img(id=f"{id}_sub_{i}",src=s, className=f"plot-img img-fluid {imgCls}" ) for i,s in enumerate(src)]
        #return html.Div(id=id,children=fhtml, className="plot-img")

    def plotToDashImg(self , p , id):
        src = self.plotToImgSrc(p)
        if type(src) != list:
            src = [src]
        fhtml = [ html.Img(id=f"{id}_sub_{i}",src=s, className="plot-img img-fluid") for i,s in enumerate(src)]
        return html.Div(id=id,children=[fhtml], className="plot-img")

    def plot_html(self,*args , **kwargs):
        p = self.plot(*args , **kwargs)
        log.info("Plot to Img Src")
        src = self.plotToImgSrc(p)
        log.info("Src to Dash Imgs")
        imgs  =self.srcToImgs(src)
        log.info("Dash Imgs to Layout")
        children = self.makePlotImgsLayout(imgs)
        return children

    def makePlotImgsLayout(self,plotImgs):
        return html.Div(children=plotImgs, className="imgs-container")

    def dashImg(self ,id=None, *args , **kwargs):
        return self.plotToDashImg(self.plot(*args , **kwargs), id)

    def dashSrc(self, *args ,**kwargs):
        return self.plotToImgSrc(self.plot(*args ,**kwargs))

    def plot(self,*args , **kwargs):
        df = self._filteredDf(*args , **kwargs)
        p = self._chart(df,*args , **kwargs)
        return p

    def setupOptions(self):
        raise NotImplementedError()

    def makeLayout(self):
        raise NotImplementedError()

    def create(self):
        self.setupOptions()
        self.makeLayout()
