# This file is the main file that is run to start the data collection and processing. It imports the necessary classes and functions from the other files and runs them.

from api.oanda_api import OandaApi # Import the OandaApi class from the api/oanda_api.py file
from infrastructure.instrument_collection import instrumentCollection # Import the instrumentCollection instance from the infrastructure/instrument_collection.py file
from stream_example.streamer import run_streamer # Import the run_price_streamer function from the stream_example/streamer.py file


if __name__ == "__main__": # If this file is run directly, do the following:
  
    # Create an instance of the OandaApi class.
    api = OandaApi()
    instrumentCollection.LoadInstruments("./data") # Load the instruments from the data directory 
    run_streamer() # Run the streamer - generate pkl's in data directory

    #stream_prices(['GBP_JPY', 'AUD_NZD']) 
    
    
    #run_collection(instrumentCollection, api) # Run the data collection - generate pkl's in data directory
    #run_ema_macd(instrumentCollection)


    #run_ema_macd(instrumentCollection) # Run the processes
    #print(api.fetch_candles("EUR_USD", granularity="D", price="MB"))
    #run_ma_sim() # Run the moving average simulation - generate xlsx file from pkl's in data directory


