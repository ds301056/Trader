from api.oanda_api import OandaApi # Import the OandaApi class from the api/oanda_api.py file
from models.candle_timing import CandleTiming # Import the CandleTiming class from the models/candle_timing.py file

class CandleManager:

  def __init__(self, api: OandaApi, trade_settings, log_message, granularity): # Initialize the CandleManager object with the api, trade_settings, log_message, and granularity parameters
    self.api = api # Set the api attribute to the value of the api parameter
    self.trade_settings = trade_settings # Set the trade_settings attribute to the value of the trade_settings parameter
    self.log_message = log_message # Set the log_message attribute to the value of the log_message parameter
    self.granularity = granularity # Set the granularity attribute to the value of the granularity parameter
    self.pairs_list = list(self.trade_settings.keys()) # Get the list of pairs from the trade settings keys
    self.timings = { p: CandleTiming(self.api.last_complete_candle(p, self.granularity)) for p in self.pairs_list } # Initialize the timings attribute as a dictionary with pairs as keys and CandleTiming objects as values
    for p, t in self.timings.items(): # Iterate over the timings dictionary
      self.log_message(f"CandleManager() init last_candle: {t}", p) # Log the initialization of the CandleTiming object



  # Update the timings for each pair in the pairs list based on the last complete candle time
  # get pair names if there is a new candle and return them
  def update_timings(self):
    triggered = []


    for pair in self.pairs_list: # Iterate over the pairs in the pairs list
      current = self.api.last_complete_candle(pair, self.granularity) # Get the last complete candle for the pair
      if current is None: # Check if the current candle is None
        self.log_message(f"unable to get candle for {pair}", pair) # Log an error message if the current candle is None
        continue
      self.timings[pair].is_ready = False # Reset the is_ready attribute to False
      if current > self.timings[pair].last_time: # Check if the current time is greater than the last time
        self.timings[pair].is_ready = True # Set the is_ready attribute to True
        self.timings[pair].last_time = current # Update the last_time attribute
        self.log_message(f"CandleManager() new candle:{self.timings[pair]}", pair) # Log the new candle timing
        triggered.append(pair) # Append the pair to the triggered list
    return triggered # Return the triggered list