import threading # Import the threading module
import requests # Import the requests module
import constants.defs as defs # Import the defs module from the constants/defs.py file
import json # Import the json module
import pandas as pd # Import the pandas module

from timeit import default_timer as timer # Import the timer function from the timeit module
from stream_example.stream_base import StreamBase # Import the StreamBase class from the stream_example/stream_base.py file


from infrastructure.log_wrapper import LogWrapper # Import the LogWrapper class from the infrastructure/log_wrapper.py file
from models.live_api_price import LiveApiPrice # Import the LiveApiPrice class from the models/live_api_price.py file



# url for live price streaming 
STREAM_URL = f"https://stream-fxpractice.oanda.com/v3"

class PriceStreamer(StreamBase): # Define a PriceStreamer class that extends the threading.Thread class

  LOG_FREQ = 60 # Set the log frequency to 100

  def __init__(self, shared_prices, price_lock: threading.Lock, price_events): # Define the __init__ method with the shared_prices, shared_prices_events, shared_prices_lock, and pairs_list arguments
    super().__init__(shared_prices, price_lock, price_events, "PriceStreamer") # Call the __init__ method of the threading.Thread class
    self.pair_list = shared_prices.keys() # Set the pair_list attribute to the keys of the shared_prices dictionary
    print(self.pair_list) # Print the pair_list


  def fire_new_price_event(self, instrument): # Define a function called fire_new_price_event that takes an instrument argument
    if self.price_events[instrument].is_set() == False:
      self.price_events[instrument].set()

  def update_live_price(self, live_price: LiveApiPrice ): # Define a function called update_live_price that takes a live_price argument
    
    try:
      self.price_lock.acquire() # Acquire the price lock
      self.shared_prices[live_price.instrument] = live_price # Set the live price instrument to the live price
      self.fire_new_price_event(live_price.instrument) # Fire a new price event
    except Exception as error:
      self.log_message(f"Exception: {error}", error=True) # Log the error
    finally:
      self.price_lock.release() # Release the price lock on the thread 

  def log_data(self): # Define a function called log_data

    self.log_message("")
    self.log_message(f"\n{pd.DataFrame.from_dict([v.get_dict() for _, v in self.shared_prices.items()])}") # Log the shared prices as a dataframe


  def run(self): # Define a function called stream_prices that takes a list of pairs as an argument


    start = timer() - PriceStreamer.LOG_FREQ + 10# Start logging prices after 10 seconds 


    params = dict( # Create a dictionary to store the parameters
      instruments=','.join(self.pair_list) # Join the pairs_list with a comma
    )

    # url for live price streaming
    url = f"{STREAM_URL}/accounts/{defs.ACCOUNT_ID}/pricing/stream"

    # Make a GET request to the url
    resp = requests.get(url, params=params, headers=defs.SECURE_HEADER, stream=True)

    for price in resp.iter_lines():
      if price:
        decoded_price = json.loads(price.decode('utf-8')) # Decode the price into json 
        if 'type' in decoded_price and decoded_price['type'] == 'PRICE':
          self.update_live_price(LiveApiPrice(decoded_price))
          if timer() - start > PriceStreamer.LOG_FREQ: # Check if the time elapsed is greater than the log frequency
            print(LiveApiPrice(decoded_price).get_dict()) # Print the LiveApiPrice object with the decoded price
            self.log_data() # Log the data
            start = timer() # Set the start time to the current time





