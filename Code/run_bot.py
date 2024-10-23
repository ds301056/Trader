from bot.bot import Bot
from infrastructure.instrument_collection import instrumentCollection # Import the instrumentCollection instance from the infrastructure/instrument_collection.py file


if __name__ == "__main__": # If the script is being run directly
  instrumentCollection.LoadInstrumentsDB() # Load the instruments from the data directory
  #print(instrumentCollection.instruments_dict)
  b = Bot() # Create a Bot object
  b.run() # Call the run method on the Bot object