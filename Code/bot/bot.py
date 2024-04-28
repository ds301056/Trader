import json # Import the json module
import time # Import the time module
import constants.defs as defs # Import the defs module from the constants/defs.py file

from bot.trade_manager import place_trade # Import the place_trade function from the bot/trade_manager.py file
from bot.technicals_manager import get_trade_decision # Import the get_trade_decision function from the bot/technicals_manager.py file
from bot.candle_manager import CandleManager # Import the CandleManager class from the bot/candle_manager.py file
from infrastructure.log_wrapper import LogWrapper # Import the LogWrapper class from the infrastructure/log_wrapper.py file
from models.trade_settings import TradeSettings # Import the TradeSettings class from the models/trade_settings.py file
from api.oanda_api import OandaApi # Import the OandaApi class from the api/oanda_api.py file
from infrastructure.main_log_handler import MainLogHandler  # Assuming MainLogHandler is in infrastructure folder




class Bot:

  #constants
  ERROR_LOG = "error"
  MAIN_LOG = "main"
  GRANULARITY = "M1"
  SLEEP = 10

  def __init__(self): # Initialize the Bot object
    self.load_settings()  # Load settings from JSON
    self.api = OandaApi()  # Create an instance of OandaApi
    self.main_log_handler = MainLogHandler()  # Initialize MainLogHandler
    self.setup_logs()  # Set up logging first before creating instances that use logging

    # Now create instances that might use logging in their constructor or methods
    self.candle_manager = CandleManager(self.api, self.trade_settings, self.log_message, Bot.GRANULARITY)
    
    self.log_to_main("Bot started")  # Log a message to the main log
    self.log_to_error("Bot started")  # Log a message to the error log




  def load_settings(self): # Define the load_settings method
    with open("./bot/settings.json", "r") as f: # Open the settings.json file in read mode
      data=json.loads(f.read()) # Load the JSON file into a dictionary
      self.trade_settings = {k: TradeSettings(v, k) for k, v in data['pairs'].items()} # Set the trade settings attribute to a dictionary of TradeSettings objects
      self.tarde_risk = data['trade_risk'] # Set the trade risk attribute to the trade risk value from the JSON file

  def setup_logs(self): # Define the setup_logs method
    self.logs = {} # Initialize the logs attribute as an empty dictionary
    for k in self.trade_settings.keys(): # Iterate over the trade settings keys
      self.logs[k] = LogWrapper(k) # Create a LogWrapper object for each trade setting key and add it to the logs dictionary
      self.log_message(f"{self.trade_settings[k]}", k) # Log the trade settings for each key

    self.logs[Bot.ERROR_LOG] = LogWrapper(Bot.ERROR_LOG) # Create a LogWrapper object for the error log and add it to the logs dictionary
    self.logs[Bot.MAIN_LOG] = LogWrapper(Bot.MAIN_LOG) # Create a LogWrapper object for the main log and add it to the logs dictionary
    self.log_to_main(f"Bot started with {TradeSettings.settings_to_str(self.trade_settings)}") # Log the trade settings for the main log

  def log_message(self, msg, key): # Define the log_message method with the msg and key parameters
    self.logs[key].logger.debug(msg) # Log the message at the debug level using the specified key

  def log_to_main(self, msg): # Define the log_to_main method with the msg parameter
    self.log_message(msg, Bot.MAIN_LOG) # Call the log_message method with the message and main log key
    self.main_log_handler.log(msg)  # Also log to the main log handler
    
  def log_to_error(self, msg): # Define the log_to_error method with the msg parameter
    self.log_message(msg, Bot.ERROR_LOG) # Call the log_message method with the message and error log key


  def process_candles(self, triggered):
      if len(triggered) > 0:
        self.log_message(f"process_candles triggered: {triggered}", Bot.MAIN_LOG)
        for p in triggered:
          last_time = self.candle_manager.timings[p].last_time # p is pair name
          trade_decision = get_trade_decision(last_time, p, Bot.GRANULARITY, self.api, self.trade_settings[p], self.log_message) # Get the trade decision

          if trade_decision is not None and trade_decision.signal != defs.NONE: # Check if the trade decision is not None and the signal is not NONE
            self.log_message(f"Place Trade: {trade_decision}", p) # Log the trade decision
            self.log_to_main(f"Place Trade: {trade_decision}") # Log the trade decision to the main log

            #place trade with trade manager 
            place_trade(trade_decision, self.api, self.log_message, self.log_to_error, self.tarde_risk) # Place the trade


  def run(self): # Define the run method
    while True:
      time.sleep(Bot.SLEEP) # Sleep for the specified time
      try: 
        self.process_candles(self.candle_manager.update_timings()) # Process the candles and update the timings
      except Exception as error:
        self.log_to_error(f"CRASH: {error}") # Log an error message if there is an exception
        break



