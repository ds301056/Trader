# import statements for the trade_manager.py file
from bot.trade_risk_calculator import get_trade_units # Import the get_trade_units function from the bot/trade_risk_calculator.py file
from api.oanda_api import OandaApi # Import the OandaApi class from the api/oanda_api.py file
from models.trade_decision import TradeDecision # Import the TradeDecision class from the models/trade_decision.py file



def trade_is_open(pair, api: OandaApi): # Define the trade_is_open function with the pair and api parameters

  open_trades = api.get_open_trades() # Get the open trades from the API

  for ot in open_trades: # Iterate over the open trades
    if ot.instrument == pair: # Check if the open trade instrument matches the pair
      return ot # Return the open trade
    
  return None # Return None if no open trade is found


def place_trade(trade_decision: TradeDecision, api: OandaApi, log_message, log_error, trade_risk):

  ot = trade_is_open(trade_decision.pair, api) # Check if the trade is already open

  if ot is not None: # If the trade is already open
    log_message(f"Failed to place trade {trade_decision}, already open: {ot}", trade_decision.pair) # Log a message that the trade is already open
    return None # Return None
  

  trade_units = get_trade_units(api, trade_decision.pair, trade_decision.signal, trade_decision.loss, trade_risk, log_message) # Get the trade units


  trade_id = api.place_trade( # Place the trade
    trade_decision.pair, 
    trade_units,
    trade_decision.signal,
    trade_decision.sl,
    trade_decision.tp
  )

  if trade_id is None:
    log_error(f"ERROR placing {trade_decision}") # Log an error message if the trade placement fails
    log_message(f"ERROR placing {trade_decision}", trade_decision.pair) # Log an error message if the trade placement fails

  else:
    log_message(f"Placed trade_id:{trade_id} for {trade_decision}", trade_decision.pair)


