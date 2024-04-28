from dateutil import parser  # Used for parsing dates

class OpenTrade:
    def __init__(self, api_obj): # Initialize the OpenTrade object with the api_obj parameter
        self.id = api_obj['id'] # Set the id attribute to the value of the 'id' key in the api_obj dictionary
        self.instrument = api_obj['instrument'] # Set the instrument attribute to the value of the 'instrument' key in the api_obj dictionary
        self.price = float(api_obj['price']) # Set the price attribute to the value of the 'price' key in the api_obj dictionary
        self.currentUnits = float(api_obj['currentUnits']) # Set the currentUnits attribute to the value of the 'currentUnits' key in the api_obj dictionary
        self.unrealizedPL = float(api_obj['unrealizedPL']) # Set the unrealizedPL attribute to the value of the 'unrealizedPL' key in the api_obj dictionary
        self.marginUsed = float(api_obj['marginUsed']) # Set the marginUsed attribute to the value of the 'marginUsed' key in the api_obj dictionary

    def __repr__(self): # Define the __repr__ method to return a string representation of the OpenTrade object
        return str(vars(self)) # Return the string representation of the OpenTrade object