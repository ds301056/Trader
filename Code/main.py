from api.oanda_api import OandaApi # Import the OandaApi class from the api/oanda_api.py file
from infrastructure.instrument_collection import instrumentCollection # Import the instrumentCollection instance from the infrastructure/instrument_collection.py file
from simulation.ma_cross import run_ma_sim # Import the run_ma_sim function from the simulation/ma_cross.py file

if __name__ == "__main__": # If this file is run directly, do the following:
  
    # Create an instance of the OandaApi class.
    api = OandaApi()
    
    #instrumentCollection.CreateFile(api.get_account_instruments(), "./data")
    #instrumentCollection.LoadInstruments("./data") # Load the instruments from the instruments.json file
    #instrumentCollection.PrintInstruments() # Print the instruments

    run_ma_sim(curr_list=["EUR", "USD", "GBP"]) # Run the moving average simulation




   
    
