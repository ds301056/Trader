

class TradeSettings: # Define the TradeSettings class

  def __init__(self, ob, pair): # Initialize the TradeSettings object with the ob and pair parameters
    self.n_ma = ob['n_ma'] # Set the n_ma attribute to the value of the 'n_ma' key in the ob dictionary
    self.n_std = ob['n_std'] # Set the n_std attribute to the value of the 'n_std' key in the ob dictionary
    self.maxspread = ob['maxspread'] # Set the maxspread attribute to the value of the 'maxspread' key in the ob dictionary
    self.mingain = ob['mingain'] # Set the mingain attribute to the value of the 'mingain' key in the ob dictionary
    self.riskreward = ob['riskreward'] # Set the riskreward attribute to the value of the 'riskreward' key in the ob dictionary

  def __repr__(self): # Define the __repr__ method to return a string representation of the TradeSettings object  
    return str(vars(self)) # Return the string representation of the TradeSettings object
  
  @classmethod
  def settings_to_str(cls, settings): # Define the settings_to_str class method with the settings parameter
    ret_str = "Trade Settings:\n"
    for _, v in settings.items():
      ret_str += f"{v}\n" # Append the string representation of each setting to the return string


    return ret_str # Return the final string representation of the trade settings
