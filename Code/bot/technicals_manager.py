import pandas as pd # Import the pandas library
import constants.defs as defs # Import the defs module from the constants/defs.py file

from models.trade_decision import TradeDecision # Import the TradeDecision class from the models/trade_decision.py file
from api.oanda_api import OandaApi # Import the OandaApi class from the api/oanda_api.py file
from models.trade_settings import TradeSettings # Import the TradeSettings class from the models/trade_settings.py file
from technicals.indicators import BollingerBands # Import the BollingerBands function from the technicals/indicators.py file


#pandas settings / options : set columns to display ie all of them 
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False) # Set the expand_frame_repr option to False - keep all information on one line (no wrapping)


ADDROWS = 20 # Add rows to the moving average


def apply_signal(row, trade_settings: TradeSettings): # Define the apply_signal function with the row and trade_settings parameters
  if row.SPREAD <= trade_settings.maxspread and row.GAIN >= trade_settings.mingain:
    if row.mid_c > row.BB_UP and row.mid_o < row.BB_UP: #signal to sell
      return defs.SELL
    elif row.mid_c < row.BB_LW and row.mid_o > row.BB_LW: #signal to buy 
      return defs.BUY 
  return defs.NONE # Return nothing
    

def apply_SL(row, trade_settings: TradeSettings): # Define the apply_SL function with the row and trade_settings parameters
  if row.SIGNAL == defs.BUY: # Check if the signal is to buy
    return row.mid_c - (row.GAIN / trade_settings.riskreward) # Return the stop loss for buying
  elif row.SIGNAL == defs.SELL: # Check if the signal is to sell
    return row.mid_c + (row.GAIN / trade_settings.riskreward) # Return the stop loss for selling
  return 0.0 # Return 0.0

def apply_TP(row):
  if row.SIGNAL == defs.BUY: # Check if the signal is to buy
    return row.mid_c + row.GAIN # Return the take profit for the row
  elif row.SIGNAL == defs.SELL: # Check if the signal is to sell
    return row.mid_c - row.GAIN # Return the take profit for the row
  return 0.0 # Return 0.0


def process_candles(df: pd.DataFrame, pair, trade_settings: TradeSettings, log_message): # Define the process_candles function with the df, pair, trade_settings, and log_message parameters

  df.reset_index(drop=True, inplace=True) # Reset the index of the dataframe and modify it in place (drop the old index)
  df['PAIR'] = pair # Add a column to the dataframe with the pair name
  df['SPREAD'] = df.ask_c - df.bid_c # Add a column to the dataframe with the spread

  #Make the indicators


  df = BollingerBands(df, trade_settings.n_ma, trade_settings.n_std) # Calculate the Bollinger Bands
  df['GAIN'] = abs(df.mid_c - df.BB_MA) # Calculate the gain: mid c - bb moving average 
  df['SIGNAL'] = df.apply(apply_signal, axis=1, trade_settings=trade_settings) # Apply the signal to the dataframe
  df['TP'] = df.apply(apply_TP, axis=1) # Apply the take profit to the dataframe
  df['SL'] = df.apply(apply_SL, axis=1, trade_settings=trade_settings) # Apply the stop loss to the dataframe
  df['LOSS'] = abs(df.mid_c - df.SL) # Calculate the loss: mid c - stop loss

  log_cols = ['PAIR', 'time', 'mid_c', 'mid_o', 'SL', 'TP', 'SPREAD', 'GAIN', 'LOSS', 'SIGNAL'] # Define the columns to log
  log_message(f"process_candles:\n{df[log_cols].tail()}", pair) # Log the last rows of the dataframe with the specified columns

  return df[log_cols].iloc[-1] # Return the signal for the last row of the dataframe

def fetch_candles(pair, row_count, candle_time, granularity, api: OandaApi, log_message): # Define the fetch_candles function with the pair, row_count, candle_time, granularity, api, and log_message parameters
  df = api.get_candles_df(pair, count=row_count, granularity=granularity) # Get the candles dataframe for the pair, row count, and granularity  

  if df is None or df.shape[0] == 0:
    log_message("tech_manager fetch_candles failed to get candles. ie: no data", pair) # Log a message if there is no data
    return None # Return None
  
  if df.iloc[-1].time != candle_time: # Check if the last candle time is not equal to the current candle time
    log_message(f"tech_manager fetch_candles candle time mismatch. ie: {df.iloc[-1].time} not correct", pair)
    return None # Return None

  return df # Return the candles dataframe


# can we trade? yes or no
def get_trade_decision(candle_time, pair, granularity, api: OandaApi, trade_settings: TradeSettings, log_message):



  max_rows = trade_settings.n_ma + ADDROWS # Get the maximum number of rows for the moving average

  log_message(f"tech_manager: max_rows:{max_rows} candle_time{candle_time} granularity:{granularity}", pair) # Log the trade decision
  
  df = fetch_candles(pair, max_rows, candle_time, granularity, api, log_message) # Get the candles dataframe

  if df is not None: # Check if the dataframe is None
    last_row = process_candles(df, pair, trade_settings, log_message) # Process the candles
    return TradeDecision(last_row) # Return the trade decision
  
  return None # Return None