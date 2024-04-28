from api.oanda_api import OandaApi # Import the OandaApi class from the api/oanda_api.py file
from infrastructure.instrument_collection import instrumentCollection as ic # Import the instrumentCollection instance from the infrastructure/instrument_collection.py file

import constants.defs as defs # Import the defs module from the constants/defs.py file


def get_trade_units(api: OandaApi, pair, signal, loss, trade_risk, log_message):

  prices = api.get_prices([pair]) # Get the prices for the pair

  if prices is None or len(prices) == 0: # Check if the prices are None or empty
    log_message("get_trade_units() Prices is none", pair) # Log a message that the prices are None
    return False # Return False 

  price = None # Initialize the price variable as None
  for p in prices: # Iterate over the prices
    if p.instrument == pair: # Check if the price instrument matches the pair
      price = p # Set the price to the current price
      break # Break the loop

  if price is None: # Check if the price is None
    log_message("get_trade_units() Price is none????", pair) # Log a message that the price is None
    return False # Return False
  
  log_message(f"get_trade_units() Price is {price}", pair) # Log the price

  conv = price.buy_conv # Set the conversion to the buy conversion
  if signal == defs.SELL: # Check if the signal is to sell
    conv = price.sell_conv # Set the conversion to the sell conversion

  pipLocation = ic.instruments_dict[pair].pipLocation # Get the pip location for the pair
  num_pips = loss / pipLocation # Calculate the number of pips
  per_pip_loss = trade_risk / num_pips # Calculate the per pip loss
  units = per_pip_loss / (conv * pipLocation) # Calculate the units based on the conversion and pip location


  log_message(f"{pipLocation} {num_pips} {per_pip_loss} {units:.1f}", pair) # Log the pip location, number of pips, per pip loss, and units


  return units # Return the units