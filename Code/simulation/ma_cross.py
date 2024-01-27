# Importing necessary libraries
import pandas as pd  # pandas for data manipulation and analysis
from infrastructure.instrument_collection import instrumentCollection as ic  # importing instrumentCollection from infrastructure



class MAResult:  # Class to represent the result of a moving average simulation
    def __init__(self, df_trades, pairname, ma_l, ma_s, granularity):  # Constructor for the MAResult class
        self.pairname = pairname  # Currency pair name
        self.df_trades = df_trades  # Dataframe containing the trades
        self.ma_l = ma_l  # Long moving average period
        self.ma_s = ma_s  # Short moving average period
        self.granularity = granularity  # Granularity of the price data
        self.result = self.result_ob()  # Result object


    def __repr__(self): # Function to return a string representation of the MAResult object
        return str(self.result) # Return the result object as a string
    

    def result_ob(self):
        return dict(
            pair=self.pairname,
            num_trades=self.df_trades.shape[0],
            total_gain=self.df_trades.GAIN.sum(),
            mean_gain=self.df_trades.GAIN.mean(),
            min_gain=self.df_trades.GAIN.min(),
            max_gain=self.df_trades.GAIN.max(),
            ma_l=self.ma_l,
            ma_s=self.ma_s
            
        )
        
      



# Constants for trade signals
BUY = 1     # Constant to represent a BUY signal
SELL = -1   # Constant to represent a SELL signal
NONE = 0    # Constant to represent no action (NONE)

# Lambda function to format moving average column names
get_ma_col = lambda x: f"MA_{x}"  # A function to create a string for moving average column name based on a given period x


def is_trade(row):  # Function to determine if a trade should be made based on the moving average delta
    if row["DELTA"] >= 0 and row["DELTA_PREV"] < 0:  # If the delta is positive and the previous delta is negative
        return BUY  # Return a BUY signal
    elif row["DELTA"] < 0 and row["DELTA_PREV"] > 0:  # If the delta is negative and the previous delta is positive
        return SELL  # Return a SELL signal
    else:  # Otherwise
        return NONE  # Return no action (NONE)



"""
:Function to load price data for a given currency pair and granularity.
:param pair: Currency pair to load price data for.
:param granularity: Granularity of the price data.
:param ma_list: List of moving average periods to calculate.
:return: A dataframe containing the price data and moving averages.
"""
def load_price_data(pair, granularity, ma_list):  # Function to load price data for a given currency pair and granularity

    df = pd.read_pickle(f"./data/{pair}_{granularity}.pkl")  # Load the price data from the pickle file
    for ma in ma_list: # Iterate through each moving average period
        df[get_ma_col(ma)] = df.mid_c.rolling(window=ma).mean()  # Calculate the moving average and add it to the dataframe
    df.dropna(inplace=True)  # Drop any rows with missing values
    df.reset_index(drop=True, inplace=True)  # Reset the index of the dataframe
    return df  # Return the dataframe




def get_trades(df_analysis, instrument): # Function to calculate the trades and total gain
    df_trades = df_analysis[df_analysis.TRADE != NONE].copy() # Filter the dataframe to only include rows with a trade signal
    df_trades["DIFF"] = df_trades.mid_c.diff().shift(-1) # Calculate the difference between the current and next closing price
    df_trades.fillna(0, inplace=True) # Fill any missing values with 0
    df_trades["GAIN"] = df_trades.DIFF / instrument.pipLocation # Calculate the gain in pips
    df_trades["GAIN"] = df_trades["GAIN"] * df_trades["TRADE"] # Multiply the gain by the trade signal
    return df_trades # Return the total gain and the trades dataframe







def assess_pair(price_data, ma_l, ma_s, instrument): # Function to assess a currency pair for a given granularity and moving averages
    df_analysis = price_data.copy() # Create a copy of the price data
    df_analysis["DELTA"] = df_analysis[ma_s] - df_analysis[ma_l] # Calculate the delta between the moving averages
    df_analysis["DELTA_PREV"] = df_analysis["DELTA"].shift(1) # Shift the delta by 1 row
    df_analysis["TRADE"] = df_analysis.apply(is_trade, axis=1) # Apply the is_trade function to the dataframe
    
    df_trades = get_trades(df_analysis, instrument) # Return the trades and total gain
    return MAResult(
        df_trades,
        instrument.name,
        ma_l,
        ma_s
    ) # Return the MAResult object



def process_results(results_list): # Function to process the results
    rl = [x.result for x in results_list] # Create a list of the result objects
    df = pd.DataFrame.from_dict(rl) # Create a dataframe from the result objects
    print(df)








def analyse_pair(instrument, granularity, ma_long, ma_short):  # Function to analyse a currency pair for a given granularity and moving averages
    ma_list = set(ma_long + ma_short) # Create a set of the moving average periods
    pair = instrument.name # Get the currency pair name

    price_data = load_price_data(pair, granularity, ma_list) # Load the price data for the currency pair and granularity
    #print(pair) # Print the currency pair
    #print(price_data.head(3)) # Print the first 3 rows of the price data 



    results_list = [] # Create an empty list to store the results







    for ma_l in ma_long: # Iterate through each long moving average period
        for ma_s in ma_short: # Iterate through each short moving average period
            if ma_l <= ma_s: # If the long moving average period is less than or equal to the short moving average period
                continue # Skip the current iteration

            ma_result = assess_pair( # Call the assess_pair function
                price_data,  # Passing the price data  
                get_ma_col(ma_l),  # Passing the column name for the long moving average
                get_ma_col(ma_s),  # Passing the column name for the short moving average
                instrument  # Passing the instrument
            )  


            print(ma_result) # Print the result
            results_list.append(ma_result) # Append the result to the results list
    process_results(results_list) # Call the process_results function

            

        




# Main function to run moving average simulation
def run_ma_sim(curr_list=["EUR", "USD"],  # Default currency list (can be modified
               granularity=["H1", "H4"],       # Default granularity list (can be modified)
               ma_long=[20, 40, 80],      # Default values for long moving averages (can be modified)
               ma_short=[10, 20]):        # Default values for short moving averages (can be modified)
    """
    Function to run a moving average simulation.
    :param curr_list: List of currencies to consider in the simulation.
    :param granularity: Time granularity for the simulation.
    :param ma_long: Periods for long-term moving averages.
    :param ma_short: Periods for short-term moving averages.
    """

    # Load instrument data
    ic.LoadInstruments("./data")  # Loading instrument data from the specified path

    # Looping through the granularity, currencies, and moving average parameters
    for g in granularity:  # Iterating through each granularity level
        for p1 in curr_list:  # Iterating through each currency in the currency list
            for p2 in curr_list:  # Iterating through the currency list again for currency pairs
                pair = f"{p1}_{p2}"  # Creating a currency pair string
                if pair in ic.instruments_dict.keys():  # Checking if the currency pair is in the instrument collection
                    analyse_pair(ic.instruments_dict[pair], g, ma_long, ma_short) # Calling the analyse_pair function
                    # Analysis logic will go here, analyzing the currency pair for the given granularity and moving averages
