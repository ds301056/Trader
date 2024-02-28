from api.oanda_api import OandaApi # Import the OandaApi class from the api/oanda_api.py file
from infrastructure.instrument_collection import instrumentCollection # Import the instrumentCollection instance from the infrastructure/instrument_collection.py file
from simulation.ma_cross import run_ma_sim # Import the run_ma_sim function from the simulation/ma_cross.py file
from dateutil import parser # Import the parser module from the dateutil package
from infrastructure.collect_data import run_collection # Import the run_collection function from the infrastructure/collect_data.py file


if __name__ == "__main__": # If this file is run directly, do the following:
  
    # Create an instance of the OandaApi class.
    #api = OandaApi()

    #instrumentCollection.LoadInstruments("./data") # Load the instruments from the data directory
    #run_collection(instrumentCollection, api) # Run the data collection


    run_ma_sim() # Run the moving average simulation


