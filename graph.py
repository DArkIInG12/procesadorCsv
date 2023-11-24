import cufflinks as cf
from IPython.display import display,HTML
import plotly as py
import pandas as pd

cf.set_config_file(sharing='public',theme='white',offline=True)

def build_plot(dataframe: pd.DataFrame,x_axis,y_axis,data,name):
    df = dataframe.pivot(index=x_axis,columns=data,values=y_axis)
    fig = df.iplot(kind='bar',xTitle=x_axis,yTitle=y_axis,asFigure=True,title=name)
    py.offline.plot(fig)