import datetime as dt # Import the datetime module

class CandleTiming: # Define the CandleTiming class

  def __init__(self, last_time): # Initialize the CandleTiming object with the last_time parameter
    self.last_time = last_time # Set the last_time attribute to the value of the last_time parameter
    self.is_ready = False # Set the is_ready attribute to False

  def __repr__(self): 
    # Return the string representation of the CandleTiming object
    return f"last_candle:{dt.datetime.strftime(self.last_time, '%Y-%m-%d %H:%M')} is_ready:{self.is_ready}" 