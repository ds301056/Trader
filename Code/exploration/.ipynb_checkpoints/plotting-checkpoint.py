import datetime as dt
import plotly.graph_objects as go

class CandlePlot:

  def __init__(self, df):
    self.df_plot = df.copy()


  def create_candle_fig(self):
      fig = go.Figure(data=[go.Candlestick(x=self.df_plot['time'],
                  open=self.df_plot['open'],
                  high=self.df_plot['high'],
                  low=self.df_plot['low'],
                  close=self.df_plot['close'])])
