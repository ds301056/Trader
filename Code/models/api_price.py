
# old class _ we made changes to incorporate the homeConversion 

""" 
class Api_Price:

    def __init__(self, api_ob):
      self.instrument = api_ob['instrument'] # Set the instrument attribute to the instrument value from the API object
      self.ask = float(api_ob['asks'][0]['price']) # Set the ask attribute to the ask price from the API object
      self.bid = float(api_ob['bids'][0]['price']) # Set the bid attribute to the bid price from the API object
      self.sell_conv = float(api_ob['quoteHomeConversionFactors']['negativeUnits']) # Set the sell conversion attribute to the negative units from the API object  
      self.buy_conv = float(api_ob['quoteHomeConversionFactors']['positiveUnits']) # Set the buy conversion attribute to the positive units from the API object

    def __repr__(self):
      # Return a string representation of the ApiPrice object with the instrument, ask, bid, sell conversion, and buy conversion
      return f"Api_price() {self.instrument} ask: {self.ask} bid: {self.bid} sell_conv: {self.sell_conv:.6f} buy_conv: {self.buy_conv:.6f}" 
"""
from models.base_api_price import BaseApiPrice # Import the BaseApiPrice class from the base_api_price.py file

class Api_Price(BaseApiPrice):

  def __init__(self, api_ob, homeConversions):
   

    super().__init__(api_ob) # Call the __init__ method of the BaseApiPrice class with the api_ob argument
    # get instruments from their pair by underscore " _" 
    base_instrument = self.instrument.split('_')[1] # Get the base instrument from the instrument
    for hc in homeConversions: # Iterate over the home conversions
      if hc['currency'] == base_instrument: # Check if the home conversion currency matches the base instrument
        self.sell_conv = float(hc['positionValue']) # Set the sell conversion attribute to the position value
        self.buy_conv = float(hc['positionValue']) # Set the buy conversion attribute to the position value
   
   

  def __repr__(self):
    # Return a string representation of the ApiPrice object with the instrument, ask, bid, sell conversion, and buy conversion
    return f"Api_price() {self.instrument} ask: {self.ask} bid: {self.bid} sell_conv: {self.sell_conv:.6f} buy_conv: {self.buy_conv:.6f}" 


