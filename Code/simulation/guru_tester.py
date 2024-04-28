import pandas as pd # Import pandas library
import datetime as dt # Import datetime module

# Define constants for BUY, SELL, and NONE signals
BUY = 1
SELL = -1
NONE = 0

def apply_take_profit(row, PROFIT_FACTOR):
    # This function calculates the take profit target price based on a PROFIT_FACTOR multiplier
    if row.SIGNAL != NONE:
        # Only proceed if there is a trading signal (neither buy nor sell signal)
        if row.SIGNAL == BUY:
            # If the signal is to buy
            if row.direction == BUY:
                # And if the actual trading direction matches BUY
                return (row.ask_c - row.ask_o) * PROFIT_FACTOR + row.ask_c
                # Calculate profit target: (current ask price - opening ask price) * profit factor + current ask price
            else:
                # If the direction is not BUY, presumably SELL
                return (row.ask_o - row.ask_c) * PROFIT_FACTOR + row.ask_o
                # Calculate a different kind of profit target: (opening ask price - current ask price) * profit factor + opening ask price
        else:
            # If the signal is to sell
            if row.direction == SELL:
                # And if the trading direction is SELL
                return (row.bid_c - row.bid_o) * PROFIT_FACTOR + row.bid_c
                # Calculate profit target: (current bid price - opening bid price) * profit factor + current ask price
            else:
                # If the direction is not SELL, presumably BUY
                return (row.bid_o - row.bid_c) * PROFIT_FACTOR + row.bid_o
                # Calculate a different kind of profit target: (opening bid price - current bid price) * profit factor + opening ask price
    else:
        # If there is no signal, return 0.0, indicating no profit target
        return 0.0


def apply_stop_loss(row):
    # This function calculates the stop loss price based on the trading direction and signal
    if row.SIGNAL != NONE:
        # Only proceed if there is a trading signal (neither buy nor sell signal)
        if row.SIGNAL == BUY:
            # If the signal is to buy
            if row.direction == BUY:
                # And if the trading direction matches BUY
                return row.ask_o
                # Set the stop loss at the opening ask price
            else:
                # If the trading direction is not BUY, presumably SELL
                return row.ask_c
                # Set a different kind of stop loss at the current ask price
        else:
            # If the signal is to sell
            if row.direction == SELL:
                # And if the trading direction matches SELL
                return row.bid_o
                # Set the stop loss at the opening bid price
            else:
                # If the trading direction is not SELL, presumably BUY
                return row.bid_c
                # Set a different kind of stop loss at the current bid price
    else:
        # If there is no signal, return 0.0, indicating no stop loss
        return 0.0


# Function to remove spreads by equating ask and bid prices to mid prices
def remove_spread(df):
    for a in ["ask", "bid"]: # Loop over ask and bid
        for b in ["o", "h", "l", "c"]: # Loop over open, high, low, close
            c = f"{a}_{b}" # Construct column name
            df[c] = df[f"mid_{b}"] # Assign mid price to both ask and bid prices

# Function to apply trading signals and calculate TP (Take Profit) and SL (Stop Loss)
def apply_signals(df, PROFIT_FACTOR, sig): #sig() is a function not an argument - pretty cool
    df["SIGNAL"] = df.apply(sig, axis=1) # Apply trading signal function
    df["TP"] = df.apply(apply_take_profit, axis=1, PROFIT_FACTOR=PROFIT_FACTOR) # Calculate take profit
    df["SL"] = df.apply(apply_stop_loss, axis=1) # Calculate stop loss

# Function to create signals DataFrame with adjustments for M5 granularity
def create_signals(df, time_d=1):
    df_signals = df[df.SIGNAL != NONE].copy() # Filter rows with signals
    df_signals['m5_start'] = [x + dt.timedelta(hours=time_d) for x in df_signals.time] # Adjust time for M5 granularity
    # Drop unnecessary columns
    df_signals.drop(['time', 'mid_o', 'mid_h', 'mid_l', 'bid_o', 'bid_h', 'bid_l', 'ask_o', 'ask_h', 'ask_l', 'direction'], axis=1, inplace=True)
    # Rename columns for clarity
    df_signals.rename(columns={
        'bid_c' : 'start_price_BUY',
        'ask_c' : 'start_price_SELL',
        'm5_start' : 'time'
    }, inplace=True)
    return df_signals

# Trade class to encapsulate trading logic for individual trades
class Trade:
    def __init__(self, row, profit_factor, loss_factor):
        self.running = True # Flag to indicate if the trade is still open
        self.start_index_m5 = row.name # Index of the trade's starting row
        self.profit_factor = profit_factor # Multiplier for take profit
        self.loss_factor = loss_factor # Multiplier for stop loss
        # Set start and trigger prices based on the signal
        if row.SIGNAL == BUY:
            self.start_price = row.start_price_BUY
            self.trigger_price = row.start_price_BUY
        if row.SIGNAL == SELL:
            self.start_price = row.start_price_SELL
            self.trigger_price = row.start_price_SELL
        self.SIGNAL = row.SIGNAL # Store the signal type
        self.TP = row.TP # Take profit value
        self.SL = row.SL # Stop loss value
        self.result = 0.0 # Result of the trade (profit or loss)
        self.end_time = row.time # End time of the trade
        self.start_time = row.time # Start time of the trade
        
    # Method to close a trade, setting final values
    def close_trade(self, row, result, trigger_price):
        self.running = False # Mark the trade as closed
        self.result = result # Set the result (profit or loss)
        self.end_time = row.time # Update the end time
        self.trigger_price = trigger_price # Update the trigger price
        
    # Method to update the trade based on new row data
    def update(self, row):
        # BUY logic: check if the bid high crosses take profit or bid low crosses stop loss
        if self.SIGNAL == BUY:
            if row.bid_h >= self.TP:
                self.close_trade(row, self.profit_factor, row.bid_h)
            elif row.bid_l <= self.SL:
                self.close_trade(row, self.loss_factor, row.bid_l)
        # SELL logic: check if the ask low crosses take profit or ask high crosses stop loss
        if self.SIGNAL == SELL:
            if row.ask_l <= self.TP:
                self.close_trade(row, self.profit_factor, row.ask_l)
            elif row.ask_h >= self.SL:
                self.close_trade(row, self.loss_factor, row.ask_h)

# GuruTester class to encapsulate the testing logic for the trading strategy
class GuruTester:
    def __init__(self, df_big, apply_signal, df_m5, use_spread=True, LOSS_FACTOR=-1.0, PROFIT_FACTOR=1.5, time_d=1):
        self.df_big = df_big.copy() # Copy of the larger timeframe DataFrame
        self.use_spread = use_spread # Flag to indicate whether to adjust for spread
        self.apply_signal = apply_signal # Function to apply trading signals
        self.df_m5 = df_m5.copy() # Copy of the M5 timeframe DataFrame
        self.LOSS_FACTOR = LOSS_FACTOR # Multiplier for stop loss
        self.PROFIT_FACTOR = PROFIT_FACTOR # Multiplier for take profit
        self.time_d = time_d # Time delta for adjusting signal times
        self.prepare_data() # Prepare data for testing
        
    # Method to prepare data by removing spread and applying signals
    def prepare_data(self):

        #print("Preparing data...") # just so i know its happening


        if self.use_spread == False:
            remove_spread(self.df_big) # Remove spread from the larger timeframe DataFrame
            remove_spread(self.df_m5) # Remove spread from the M5 timeframe DataFrame

        apply_signals(self.df_big, self.PROFIT_FACTOR, self.apply_signal) # Apply signals to the larger timeframe DataFrame
        
        df_m5_slim = self.df_m5[['time','bid_h', 'bid_l', 'ask_h', 'ask_l']].copy() # Create a slimmed down DataFrame for M5
        df_signals = create_signals(self.df_big, time_d=self.time_d) # Create signals DataFrame
        
        # Merge M5 slim DataFrame with signals DataFrame
        self.merged = pd.merge(left=df_m5_slim, right=df_signals, on='time', how='left')
        self.merged.fillna(0, inplace=True) # Fill NaN values with 0
        
        # Convert SIGNAL and start_index_h1 columns to integer type
        self.merged.SIGNAL = self.merged.SIGNAL.astype(int)

    # Method to run the test, evaluating trades and computing results
    def run_test(self):

        #print("run_test...") # just so i know its happening

        open_trades_m5 = [] # List to store open trades
        closed_trades_m5 = [] # List to store closed trades
        # Iterate through merged DataFrame rows
        for index, row in self.merged.iterrows():
            # If there's a trading signal, create a new Trade instance
            if row.SIGNAL != NONE:
                open_trades_m5.append(Trade(row, self.PROFIT_FACTOR, self.LOSS_FACTOR))  
            # Update and possibly close open trades
            for ot in open_trades_m5:
                ot.update(row)
                if ot.running == False:
                    closed_trades_m5.append(ot) # Move closed trades to closed_trades_m5 list
            # Filter to keep only still-open trades
            open_trades_m5 = [x for x in open_trades_m5 if x.running == True]
        # Create a DataFrame from closed trades data
        self.df_results = pd.DataFrame.from_dict([vars(x) for x in closed_trades_m5])
        
        #print("Result:", self.df_results.result.sum()) # just for debugging
