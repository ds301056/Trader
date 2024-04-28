
from dateutil import parser # Import the parser module from the dateutil package
from models.base_api_price import BaseApiPrice # Import the BaseApiPrice class from the base_api_price.py file



class LiveApiPrice(BaseApiPrice):

  def __init__(self, api_ob): # Define the __init__ method with the api_ob argument
    super().__init__(api_ob)
    self.time = parser.parse(api_ob['time']) # Set the time attribute to the time value from the API object

  def __repr__(self): # Define the __repr__ method
    
    # Return a string representation of the LiveApiPrice object with the instrument, ask, and bid
    return f"LiveApiPrice() {self.instrument} ask: {self.ask} bid: {self.bid}" 
  
  def get_dict(self): # Define the get_dict method
    return dict( # Return a dictionary with the instrument, time, ask, and bid
      instrument=self.instrument,
      time=self.time,
      ask=self.ask,
      bid=self.bid
    )