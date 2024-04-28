from api.oanda_api import OandaApi # Import the OandaApi class from the api/oanda_api.py file
from infrastructure.instrument_collection import instrumentCollection # Import the instrumentCollection instance from the infrastructure/instrument_collection.py file
from models.candle_timing import CandleTiming # Import the CandleTiming class from the models/candle_timing.py file
from bot.trade_risk_calculator import get_trade_units # Import the get_trade_units function from the bot/trade_risk_calculator.py file


import constants.defs as defs # Import the defs module from the constants/defs.py file
import time # Import the time module


# log message 
def lm(msg, pair):
    #print(msg, pair)
    pass

if __name__ == "__main__": # If this file is run directly, do the following:
  
    # Create an instance of the OandaApi class.
    api = OandaApi()

    # fetch instruments from api and save to instruments json file in data directory
    #instrumentCollection.CreateFile(api.get_account_instruments(), "./data") 

    # Load the instruments from the data directory
    instrumentCollection.LoadInstruments("./data") 


    #print(api.get_prices(["GBP_JPY"]))
    print("GBP_JPY",get_trade_units(api, "GBP_JPY", defs.BUY, 0.4, 20, lm))
    print("AUD_NZD",get_trade_units(api, "AUD_NZD", defs.BUY, 0.004, 20, lm))
    print("USD_CAD",get_trade_units(api, "USD_CAD", defs.BUY, 0.004, 20, lm))




    # place trade
    #trade_id = api.place_trade("AUD_JPY", 100, 1) #1 for buy and -1 for sell
    #print("opened:", trade_id)
    #time.sleep(10)
    #print(f"closing trade {trade_id}", api.close_trade(trade_id)) # Close the trade

    # put print in brackets to loop print the open trades in readable format
    #[print(x) for x in api.get_open_trades()] # Print the open trades

    # close the open trades
    #[api.close_trade(x.id) for x in api.get_open_trades()] # Close the open trades

    # Testing **
    #print(api.last_complete_candle("EUR_USD", granularity="M5"))

    #dd = api.last_complete_candle("EUR_USD", granularity="M5")
    #print(CandleTiming(dd))

    # Print Prices    
    #print(api.get_prices(["GBP_JPY", "AUD_NZD"]))




# python api_tests.py