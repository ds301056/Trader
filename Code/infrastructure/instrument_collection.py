import json # Import the json module
from models.instrument import Instrument # Import the Instrument class from the models/instrument.py file

class InstrumentCollection: # Create a class to represent a collection of instruments
    FILENAME = "instruments.json" # Define the filename for the instruments file
    API_KEYS = ['name', 'type', 'displayName', 'pipLocation', 
         'displayPrecision', 'tradeUnitsPrecision', 'marginRate'] # Define the keys for the API data

    def __init__(self): # Constructor method
        self.instruments_dict = {} # Create an empty dictionary to store the instruments
        
    def LoadInstruments(self, path): # Load the instruments from a file
        self.instruments_dict = {} # Create an empty dictionary to store the instruments
        fileName = f"{path}/{self.FILENAME}" # Create the filename for the instruments file
        with open(fileName, "r") as f: # Open the file for reading
            data = json.loads(f.read()) # Load the data from the file
            for k, v in data.items(): # For each key-value pair in the data
                self.instruments_dict[k] = Instrument.FromApiObject(v) # Create an Instrument object and add it to the dictionary

    def CreateFile(self, data, path): # Create a file with the instrument data
        if data is None: # If the data is None
            print("Instrument file creation failed") # Print an error message
            return # Return
        
        instruments_dict = {} # Create an empty dictionary to store the instruments
        for i in data: # For each instrument in the data
            key = i['name'] # Set the key to the name of the instrument
            instruments_dict[key] = { k: i[k] for k in self.API_KEYS } # Set the value to a dictionary of the API keys and their values

        fileName = f"{path}/{self.FILENAME}" # Create the filename for the instruments file
        with open(fileName, "w") as f: # Open the file for writing
            f.write(json.dumps(instruments_dict, indent=2)) # Write the instruments dictionary to the file


    def PrintInstruments(self): # Print the instruments in the collection
        [print(k,v) for k,v in self.instruments_dict.items()] # Print each key-value pair in the instruments dictionary
        print(len(self.instruments_dict.keys()), "instruments") # Print the number of instruments in the collection

instrumentCollection = InstrumentCollection() # Create an instance of the InstrumentCollection class
