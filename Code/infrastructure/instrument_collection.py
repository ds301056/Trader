import json # Importing the JSON library
from models.instrument import Instrument # Importing the instrument class from the models package

class InstrumentCollection:
    FILENAME = "instruments.json"  # Filename for the instruments file
    API_KEYS = ['name', 'type', 'displayName', 'pipLocation', 'tradeUnitsPrecision', 'marginRate']  # Keys for the API response

    def __init__(self): # Constructor method to initialize an instance of the instrument_collection class
        self.instruments = [] # Initializing an empty list to store the instruments

    def LoadInstruments(self, path): # Method to load instruments from a file
        self.instruments_dict = {} # Initializing an empty dictionary to store the instruments
        fileName = f"{path}/{self.FILENAME}" # Constructing the full path to the instruments file
        with open(fileName, "r") as f: # Opening the instruments file in read mode
            data = json.loads(f.read()) # Loading the JSON data from the file
            for k,v in data.items(): # Iterating through the items in the JSON data
                self.instruments_dict[k] = Instrument.FromApiObject(v) # Creating an instrument object from the API response

    def PrintInstruments(self): # Method to print the instruments
        [print(k,v) for k,v in self.instruments_dict.items()] # Printing the instruments
        print(len(self.instruments_dict.keys()), "instruments") # Printing the number of instruments
        
instrumentCollection = InstrumentCollection() # Creating an instance of the InstrumentCollection class
            