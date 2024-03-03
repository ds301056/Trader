import datetime as dt # Python standard library datetime  module
import plotly.graph_objects as go # Import the plotly graph objects module
from plotly.subplots import make_subplots # Import the make subplots function from the plotly subplots module


class CandlePlot: # Create a class to plot candlestick charts

  def __init__(self, df, candles=True): # Create the class constructor
    self.df_plot = df.copy() # Create a copy of the dataframe
    self.candles = candles # Set the candles attribute to the candles parameter
    self.create_candle_fig() # Call the create candle figure method


  def add_timestr(self): # Create a method to add a string time column to the dataframe
      self.df_plot['sTime']=[dt.datetime.strftime(x, "s%y-%m-%d %H:%M") # Create a string time column
                   for x in self.df_plot.time] # Set the string time column to the time column
      

  def create_candle_fig(self): # Create a method to create the candlestick figure
      self.add_timestr() # Call the add time string method
      self.fig = make_subplots(specs=[[{"secondary_y": True}]]) # Create a figure with a secondary y axis
      if self.candles == True: # If the candles attribute is True
        self.fig.add_trace(go.Candlestick( # Add a candlestick trace to the figure
          x=self.df_plot.sTime, # Set the x data to the string time column
          open=self.df_plot.mid_o, # Set the open data to the mid open column
          high=self.df_plot.mid_h, # Set the high data to the mid high column
          low=self.df_plot.mid_l, # Set the low data to the mid low column
          close=self.df_plot.mid_c, # Set the close data to the mid close column
          line=dict(width=1), opacity=1, # Set the line width to 1 and the opacity to 1
          increasing_fillcolor='#24A06B', # Set the increasing fill color to green
          decreasing_fillcolor='#CC2E3C', # Set the decreasing fill color to red
          increasing_line_color='#2EC886', # Set the increasing line color to green
          decreasing_line_color='#FF3A4C', # Set the decreasing line color to red
        ))

  def update_layout(self, width, height, nticks): # Create a method to update the layout of the figure
      self.fig.update_yaxes( # Update the y axes
        gridcolor="#1f292f" # Set the grid color to dark grey
      )
      self.fig.update_xaxes( # Update the x axes
        gridcolor="#1f292f", # Set the grid color to dark grey
        rangeslider=dict(visible=False), # Set the rangeslider to not visible
        nticks=nticks # Set the number of ticks to nticks
      )

      self.fig.update_layout( # Update the layout of the figure
        width=width, # Set the width to width
        height= height, # Set the height to height
        margin=dict(l=10, r=10, b=10, t=10), # Set the margins
        paper_bgcolor="#2c303c", # Set the paper background color to dark grey 
        plot_bgcolor="#2c303c", # Set the plot background color to dark grey
        font=dict(size=8, color="#e1e1e1") # Set the font size and color
      )

  def add_traces(self, line_traces, is_sec=False): # Create a method to add line traces to the figure
      for t in line_traces: # Loop through the line traces
          self.fig.add_trace(go.Scatter( # Add a scatter trace to the figure
              x=self.df_plot.sTime, # Set the x data to the string time column
              y=self.df_plot[t], # Set the y data to the line trace column
              line=dict(width=2), # Set the line width to 2
              line_shape="spline", # Set the line shape to spline
              name="t", # Set the name to t
          ), secondary_y=is_sec) # Set the secondary y axis to is_sec
             
          

  def show_plot(self, width=900, height=500, nticks=5, line_traces=[], sec_traces=[]): # Create a method to show the plot
      self.add_traces(line_traces) # Call the add traces method
      self.add_traces(sec_traces, is_sec=True) # Call the add traces method with the is_sec parameter set to True
      self.update_layout(width, height, nticks) # Call the update layout method
      self.fig.show() # Show the figure