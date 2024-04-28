import datetime as dt # datetime module
import plotly.graph_objects as go # plotly graph objects
from plotly.subplots import make_subplots # plotly subplots

class CandlePlot: # candle plot class

    def __init__(self, df, candles=True): # class constructor
        self.df_plot = df.copy() # copy dataframe
        self.candles = candles # candles
        self.create_candle_fig() # create candle figure

    def add_timestr(self): # add time string
        self.df_plot['sTime'] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") # date time string format
                        for x in self.df_plot.time]

    def create_candle_fig(self): # create candle figure
        self.add_timestr() # add time string
        self.fig = make_subplots(specs=[[{"secondary_y": True}]]) # make subplots
        if self.candles == True: # if candles is true
            self.fig.add_trace(go.Candlestick( # add candlestick
                x=self.df_plot.sTime, # x axis
                open=self.df_plot.mid_o, # open
                high=self.df_plot.mid_h, # high
                low=self.df_plot.mid_l, # low
                close=self.df_plot.mid_c, # close
                line=dict(width=1), opacity=1, # line width and opacity
                increasing_fillcolor='#24A06B', # increasing fill color
                decreasing_fillcolor="#CC2E3C", # decreasing fill color
                increasing_line_color='#2EC886',  # increasing line color
                decreasing_line_color='#FF3A4C' # decreasing line color
            ))

    def update_layout(self, width, height, nticks): # update layout
        self.fig.update_yaxes( # update y axis
            gridcolor="#1f292f" # grid color
            )
        self.fig.update_xaxes( # update x axis
            gridcolor="#1f292f", # grid color
            rangeslider=dict(visible=False), # range slider
            nticks=nticks # number of ticks
        )

        self.fig.update_layout( # update layout
            width=width, # width
            height=height, # height
            margin=dict(l=10,r=10,b=10,t=10), # margin
            paper_bgcolor="#2c303c", # paper background color
            plot_bgcolor="#2c303c", # plot background color
            font=dict(size=8, color="#e1e1e1") # font
        )

    def add_traces(self, line_traces, is_sec=False): # add traces
        for t in line_traces: # for t in line traces
            self.fig.add_trace(go.Scatter( # add scatter
                x=self.df_plot.sTime, # x axis
                y=self.df_plot[t], # y axis
                line=dict(width=2), # line width  
                line_shape="spline", # line shape
                name=t # name
            ), secondary_y=is_sec) # secondary y

    def show_plot(self, width=900, height=400, nticks=5, line_traces=[], sec_traces=[]): # show plot
        self.add_traces(line_traces) # add traces
        self.add_traces(sec_traces, is_sec=True) # add traces
        self.update_layout(width, height, nticks) # update layout
        self.fig.show() # show figure
