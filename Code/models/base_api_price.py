

class BaseApiPrice:

  def __init__(self, api_ob):
    self.instrument = api_ob['instrument'] # Set the instrument attribute to the instrument value from the API object
    self.ask = float(api_ob['asks'][0]['price']) # Set the ask attribute to the ask price from the API object
    self.bid = float(api_ob['bids'][0]['price']) # Set the bid attribute to the bid price from the API object
   