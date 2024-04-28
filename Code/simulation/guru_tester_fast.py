# Import pandas for data manipulation and datetime for handling date and time objects
import pandas as pd
import datetime as dt


#This was a test to understand t he performance of different methods to access data in a DataFrame
# this one uses the list of arrays method

""" # Start timing using a list of arrays derived from the DataFrame.
start = timer()
# Create a list containing arrays from two DataFrame columns.
items = [df.mid_c.array, df.mid_h.array]
for index in range(ar1.shape[0]):
    # Access and compute using the list of arrays.
    val1 = items[0][index] * 12
    val2 = items[1][index] - 14
# Stop the timer and print the time taken for the list of arrays method.
print(f"items[index]    -> {(timer()-start):.4f}s")
 """

# Constants used for signaling in the trading strategy
BUY = 1 # Constant for buy signal
SELL = -1 # Constant for sell signal
NONE = 0 # Constant for no signal

# Function to calculate the take profit (TP) target based on the trading signal and a profit factor
def apply_take_profit(row, PROFIT_FACTOR):
    if row.SIGNAL != NONE:  # Checks if there is a trading signal
        if row.SIGNAL == BUY:  # If the signal is a buy
            return (row.ask_c - row.ask_o) * PROFIT_FACTOR + row.ask_c  # Calculate TP for a buy
        else:  # Else, it must be a sell signal
            return (row.bid_c - row.bid_o) * PROFIT_FACTOR + row.bid_c  # Calculate TP for a sell
    else:
        return 0.0  # If no signal, return 0.0 (no profit target)

# Function to calculate the stop loss (SL) target based on the trading signal
def apply_stop_loss(row):
    if row.SIGNAL != NONE:  # Checks if there is a trading signal
        if row.SIGNAL == BUY:  # If the signal is a buy
            return row.ask_o  # Set SL at the opening ask price
        else:  # Else, it must be a sell signal
            return row.bid_o  # Set SL at the opening bid price
    else:
        return 0.0  # If no signal, return 0.0 (no stop loss)

# Function to remove the spread from price data (bid/ask) to just use mid prices
def remove_spread(df):
    for a in ["ask", "bid"]:  # For each type of price
        for b in ["o", "h", "l", "c"]:  # For each price point (open, high, low, close)
            c = f"{a}_{b}"
            df[c] = df[f"mid_{b}"]  # Set the ask/bid price to the mid price

# Function to apply the trading signals and calculate TP and SL
def apply_signals(df, PROFIT_FACTOR, sig):
    df["SIGNAL"] = df.apply(sig, axis=1)  # Apply the signal function to determine buy/sell
    df["TP"] = df.apply(apply_take_profit, axis=1, PROFIT_FACTOR=PROFIT_FACTOR)  # Apply TP function
    df["SL"] = df.apply(apply_stop_loss, axis=1)  # Apply SL function

# Function to process signals and create a DataFrame with trade start times and prices
def create_signals(df, time_d=1):
    df_signals = df[df.SIGNAL != NONE].copy()  # Filter for rows where there's a signal
    # Create a new column for the start time of each 5-minute interval after the signal
    df_signals['m5_start'] = [x + dt.timedelta(hours=time_d) for x in df_signals.time]
    # Drop unnecessary columns for the analysis
    df_signals.drop(['time', 'mid_o', 'mid_h', 'mid_l', 'bid_o', 'bid_h', 'bid_l',
                     'ask_o', 'ask_h', 'ask_l', 'direction'], axis=1, inplace=True)
    # Rename columns for clarity
    df_signals.rename(columns={
        'bid_c': 'start_price_BUY',
        'ask_c': 'start_price_SELL',
        'm5_start': 'time'
    }, inplace=True)
    return df_signals  # Return the processed DataFrame

# Constants used as indexes in the trade and test classes
INDEX_start_price_BUY = 0 # Index for the start price of a buy trade
INDEX_start_price_SELL = 1 # Index for the start price of a sell trade
INDEX_SIGNAL = 2 # Index for the trading signal
INDEX_TP = 3 # Index for the take profit target
INDEX_SL = 4 # Index for the stop loss target
INDEX_time = 5 # Index for the time
INDEX_bid_h = 6 # Index for the high bid price
INDEX_bid_l = 7 # Index for the low bid price
INDEX_ask_h = 8 # Index for the high ask price
INDEX_ask_l = 9 # Index for the low ask price
INDEX_name = 10 # Index for the index name

# Trade class to handle individual trades during simulation
class Trade:
    def __init__(self, list_values, index, profit_factor, loss_factor):
        self.running = True  # Flag to check if the trade is still running
        self.start_index_m5 = list_values[INDEX_name][index]  # Start index for minute data
        self.profit_factor = profit_factor  # Set the profit factor for the trade
        self.loss_factor = loss_factor  # Set the loss factor for the trade
        # Set the starting and trigger prices based on the signal
        if list_values[INDEX_SIGNAL][index] == BUY:
            self.start_price = list_values[INDEX_start_price_BUY][index]
            self.trigger_price = list_values[INDEX_start_price_BUY][index]
        if list_values[INDEX_SIGNAL][index] == SELL:
            self.start_price = list_values[INDEX_start_price_SELL][index]
            self.trigger_price = list_values[INDEX_start_price_SELL][index]
        self.SIGNAL = list_values[INDEX_SIGNAL][index]  # Signal for the trade
        self.TP = list_values[INDEX_TP][index]  # Take profit target
        self.SL = list_values[INDEX_SL][index]  # Stop loss target
        self.result = 0.0  # Result of the trade (profit/loss)
        self.end_time = list_values[INDEX_time][index]  # End time of the trade
        self.start_time = list_values[INDEX_time][index]  # Start time of the trade
        
    # Method to close a trade and record the result and trigger price
    def close_trade(self, list_values, index, result, trigger_price):
        self.running = False  # Set the trade as no longer running
        self.result = result  # Record the result of the trade
        self.end_time = list_values[INDEX_time][index]  # Record the end time of the trade
        self.trigger_price = trigger_price  # Record the trigger price at closing
        
    # Method to update the trade status based on new price data
    def update(self, list_values, index):
        # Check if the current high or low prices trigger the TP or SL
        if self.SIGNAL == BUY:
            if list_values[INDEX_bid_h][index] >= self.TP:
                self.close_trade(list_values, index, self.profit_factor, list_values[INDEX_bid_h][index])
            elif list_values[INDEX_bid_l][index] <= self.SL:
                self.close_trade(list_values, index, self.loss_factor, list_values[INDEX_bid_l][index])
        if self.SIGNAL == SELL:
            if list_values[INDEX_ask_l][index] <= self.TP:
                self.close_trade(list_values, index, self.profit_factor, list_values[INDEX_ask_l][index])
            elif list_values[INDEX_ask_h][index] >= self.SL:
                self.close_trade(list_values, index, self.loss_factor, list_values[INDEX_ask_h][index])

# GuruTesterFast class to conduct a fast backtest of trading strategies
class GuruTesterFast:
    def __init__(self, df_big, apply_signal, df_m5, use_spread=True, LOSS_FACTOR=-1.0, PROFIT_FACTOR=1.5, time_d=1):
        self.df_big = df_big.copy()  # Copy of the main DataFrame for safe manipulation
        self.use_spread = use_spread  # Flag to determine if spread should be considered in the data
        self.apply_signal = apply_signal  # Reference to the function to apply trading signals
        self.df_m5 = df_m5.copy()  # Copy of the minute interval DataFrame for safe manipulation
        self.LOSS_FACTOR = LOSS_FACTOR  # Set the loss factor for the simulation
        self.PROFIT_FACTOR = PROFIT_FACTOR  # Set the profit factor for the simulation
        self.time_d = time_d  # Time delta for the signals

        self.prepare_data()  # Prepare the data for testing
        
    # Method to prepare the data by removing spreads and applying signals
    def prepare_data(self):
        if self.use_spread == False:
            remove_spread(self.df_big)  # Remove spread from the big DataFrame
            remove_spread(self.df_m5)  # Remove spread from the minute DataFrame

        apply_signals(self.df_big, self.PROFIT_FACTOR, self.apply_signal)  # Apply signals to the big DataFrame

        df_m5_slim = self.df_m5[['time', 'bid_h', 'bid_l', 'ask_h', 'ask_l']].copy()  # Copy relevant columns from minute data
        df_signals = create_signals(self.df_big, time_d=self.time_d)  # Create signals from the big DataFrame

        self.merged = pd.merge(left=df_m5_slim, right=df_signals, on='time', how='left')  # Merge minute data with signals
        self.merged.fillna(0, inplace=True)  # Fill NA values with 0 for smooth processing
        self.merged.SIGNAL = self.merged.SIGNAL.astype(int)  # Ensure SIGNAL column is integer for consistency

    # Method to run the test simulation
    def run_test(self):
        print("run_test...")
        open_trades_m5 = []  # List to keep track of open trades
        closed_trades_m5 = []  # List to keep track of closed trades

        # Create a list of references to the columns used during the test for quick access
        list_value_refs = [
            self.merged.start_price_BUY.array, # Start price for buy trades
            self.merged.start_price_SELL.array, # Start price for sell trades
            self.merged.SIGNAL.array, # Trading signal
            self.merged.TP.array, # Take profit target
            self.merged.SL.array, # Stop loss target
            self.merged.time.array, # Time index
            self.merged.bid_h.array, # High bid price
            self.merged.bid_l.array, # Low bid price
            self.merged.ask_h.array, # High ask price
            self.merged.ask_l.array, # Low ask price
            self.merged.index.array, # Index for reference
        ]

        # Iterate over all rows in the merged DataFrame
        for index in range(self.merged.shape[0]):
            if list_value_refs[INDEX_SIGNAL][index] != NONE:  # If there's a signal at the current index
                # Create a new Trade object and add it to the open trades list
                open_trades_m5.append(Trade(list_value_refs, index, self.PROFIT_FACTOR, self.LOSS_FACTOR))  
            
            # Update and manage open trades
            for ot in open_trades_m5:
                ot.update(list_value_refs, index)  # Update trade status based on new data
                if ot.running == False:  # If the trade is no longer running
                    closed_trades_m5.append(ot)  # Add it to the list of closed trades
            # Filter to keep only still-running trades in the open trades list
            open_trades_m5 = [x for x in open_trades_m5 if x.running == True]

        # Compile results from closed trades into a DataFrame
        self.df_results = pd.DataFrame.from_dict([vars(x) for x in closed_trades_m5]) 
        # Optionally print the sum of results (uncomment to use)
        # print("Result:", self.df_results.result.sum())
