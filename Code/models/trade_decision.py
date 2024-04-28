
# Import the necessary libraries and modules



class TradeDecision: 
  # Define the TradeDecision class
  def __init__(self, row): # Define the __init__ method with the row parameter
    self.gain = row.GAIN # Set the gain attribute to the GAIN value in the row
    self.loss = row.LOSS # Set the loss attribute to the LOSS value in the row
    self.signal = row.SIGNAL # Set the signal attribute to the SIGNAL value in the row
    self.sl = row.SL # Set the stop loss attribute to the SL value in the row
    self.tp = row.TP # Set the take profit attribute to the TP value in the row
    self.pair = row.PAIR # Set the pair attribute to the PAIR value in the row





  def __repr__(self):
    return f"TradeDecision(): {self.pair} dir:{self.signal} gain:{self.gain:.4f} sl:{self.sl:.4f} tp:{self.tp:.4f}"
  






