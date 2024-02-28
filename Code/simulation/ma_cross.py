import pandas as pd # Import the pandas library
import os.path # Import the os.path module
from infrastructure.instrument_collection import instrumentCollection as ic # Import the instrumentCollection instance from the infrastructure/instrument_collection.py file
from simulation.ma_excel import create_ma_res # Import the create_ma_res function from the simulation/ma_cross.py file



class MAResult: # Create a class to represent the results of the moving average simulation
    def __init__(self, df_trades, pairname, ma_l, ma_s, granularity): # Initialize the MAResult class
        self.pairname = pairname # Set the pairname attribute to the pairname parameter
        self.df_trades = df_trades # Set the df_trades attribute to the df_trades parameter
        self.ma_s = ma_s # Set the ma_s attribute to the ma_s parameter
        self.ma_l = ma_l # Set the ma_l attribute to the ma_l parameter
        self.granularity = granularity # Set the granularity attribute to the granularity parameter
        self.result = self.result_ob() # Set the result attribute to the result_ob method

    def __repr__(self): # Return the string representation of the MAResult class
        return str(self.result) # Return the string representation of the result attribute

    def result_ob(self): # Return the result object
        return dict( # Return a dictionary
            pair = self.pairname, # Set the pair key to the pairname attribute
            num_trades = self.df_trades.shape[0], # Set the num_trades key to the number of rows in the df_trades attribute
            total_gain = int(self.df_trades.GAIN.sum()), # Set the total_gain key to the sum of the GAIN column in the df_trades attribute
            mean_gain = int(self.df_trades.GAIN.mean()), # Set the mean_gain key to the mean of the GAIN column in the df_trades attribute
            min_gain = int(self.df_trades.GAIN.min()),   # Set the min_gain key to the minimum of the GAIN column in the df_trades attribute
            max_gain = int(self.df_trades.GAIN.max()),   # Set the max_gain key to the maximum of the GAIN column in the df_trades attribute
            ma_l = self.ma_l, # Set the ma_l key to the ma_l attribute
            ma_s = self.ma_s, # Set the ma_s key to the ma_s attribute
            cross = f"{self.ma_s}_{self.ma_l}", # Set the cross key to the concatenation of the ma_s and ma_l attributes
            granularity = self.granularity # Set the granularity key to the granularity attribute
        )

BUY = 1 # Set the BUY variable to 1
SELL = -1 # Set the SELL variable to -1
NONE = 0 # Set the NONE variable to 0
get_ma_col = lambda x: f"MA_{x}" # Create a lambda function that returns the string "MA_" concatenated with the input parameter
add_cross = lambda x: f"{x.ma_s}_{x.ma_l}" # Create a lambda function that returns the concatenation of the ma_s and ma_l attributes of the input parameter

def is_trade(row): # Determine if a trade should be made
    if row.DELTA >= 0 and row.DELTA_PREV < 0: # If the DELTA column is greater than or equal to 0 and the DELTA_PREV column is less than 0
        return BUY # Return BUY
    elif row.DELTA < 0 and row.DELTA_PREV >= 0: # If the DELTA column is less than 0 and the DELTA_PREV column is greater than or equal to 0
        return SELL # Return SELL
    return NONE # Return NONE

def load_price_data(pair, granularity, ma_list): # Load the price data for the pair
    df = pd.read_pickle(f"./data/{pair}_{granularity}.pkl") # Read the price data from the file
    for ma in ma_list: # For each moving average
        df[get_ma_col(ma)] = df.mid_c.rolling(window=ma).mean() # Create a column for the moving average
    df.dropna(inplace=True) # Drop the rows with missing values
    df.reset_index(drop=True, inplace=True) # Reset the index of the dataframe
    return df # Return the dataframe

def get_trades(df_analysis, instrument, granularity): # Get the trades from the analysis
    df_trades = df_analysis[df_analysis.TRADE != NONE].copy() # Create a copy of the dataframe with the TRADE column not equal to NONE
    df_trades["DIFF"] = df_trades.mid_c.diff().shift(-1) # Create a column for the difference in the mid_c column
    df_trades.fillna(0, inplace=True) # Fill the missing values with 0
    df_trades["GAIN"] = df_trades.DIFF / instrument.pipLocation # Create a column for the gain
    df_trades["GAIN"] = df_trades["GAIN"] * df_trades["TRADE"] # Multiply the GAIN column by the TRADE column
    df_trades["granularity"] = granularity # Set the granularity column to the granularity parameter
    df_trades["pair"] = instrument.name # Set the pair column to the name of the instrument
    df_trades["GAIN_C"] = df_trades["GAIN"].cumsum() # Create a column for the cumulative sum of the GAIN column
    return df_trades # Return the dataframe


def assess_pair(price_data, ma_l, ma_s, instrument, granularity): # Assess the pair
    df_analysis = price_data.copy() # Create a copy of the price data
    df_analysis["DELTA"] = df_analysis[ma_s] - df_analysis[ma_l] # Create a column for the difference between the short and long moving averages
    df_analysis["DELTA_PREV"] = df_analysis["DELTA"].shift(1) # Create a column for the previous value of the DELTA column
    df_analysis["TRADE"] = df_analysis.apply(is_trade, axis=1) # Create a column for the trade
    df_trades = get_trades(df_analysis, instrument, granularity) # Get the trades from the analysis
    df_trades["ma_l"] = ma_l # Set the ma_l column to the ma_l parameter
    df_trades["ma_s"] = ma_s # Set the ma_s column to the ma_s parameter
    df_trades["cross"] = df_trades.apply(add_cross, axis=1) # Create a column for the moving average cross
    return MAResult( # Return a MAResult object
        df_trades,  # Dataframe of trades
        instrument.name, # Name of the instrument
        ma_l, # Long moving average
        ma_s, # Short moving average
        granularity # Granularity
    )

def append_df_to_file(df, filename): # Save the dataframe to a file

    if os.path.isfile(filename): # If the file already exists, load the file into a dataframe
        fd = pd.read_pickle(filename) # Load the file into a dataframe
        df = pd.concat([fd, df]) # Concatenate the file dataframe with the new dataframe

    df.reset_index(inplace=True, drop=True) # Reset the index of the dataframe
    df.to_pickle(filename) # Save the dataframe to a file
    print(filename, df.shape) # Print the filename and the shape of the dataframe
    print(df.tail(2)) # Print the last two rows of the dataframe

def get_fullname(filepath, filename): # Get the full name of the file
    return f"{filepath}/{filename}.pkl" # Return the full name of the file

def process_macro(results_list, filename): # Process the macro results
    rl = [x.result for x in results_list] # Create a list of the results
    df = pd.DataFrame.from_dict(rl) # Create a dataframe from the list of results
    append_df_to_file(df, filename) # Save the dataframe to a file

def process_trades(results_list, filename): # Process the trades 
    df = pd.concat([x.df_trades for x in results_list]) # Concatenate the trades from the results list
    append_df_to_file(df, filename) # Save the dataframe to a file

def process_results(results_list, filepath): # Process the results
    process_macro(results_list, get_fullname(filepath, "ma_res")) # Process the macro results
    process_trades(results_list, get_fullname(filepath, "ma_trades")) # Process the trades


def analyse_pair(instrument, granularity, ma_long, ma_short, filepath): # Analyse the pair

    ma_list = set(ma_long + ma_short) # Create a set of the long and short moving averages
    pair = instrument.name # Get the name of the instrument

    price_data = load_price_data(pair, granularity, ma_list) # Load the price data for the pair

    results_list = [] # Create an empty list for the results

    for ma_l in ma_long: # For each long moving average
        for ma_s in ma_short: # For each short moving average
            if ma_l <= ma_s: # If the long moving average is less than or equal to the short moving average
                continue # Continue to the next iteration

            ma_result = assess_pair( # Assess the pair
                price_data,          # Price data
                get_ma_col(ma_l),    # Long moving average
                get_ma_col(ma_s),    # Short moving average
                instrument,          # Instrument
                granularity          # Granularity
            )
            #print(ma_result)
            results_list.append(ma_result) # Append the result to the results list
    process_results(results_list, filepath) # Process the results


def run_ma_sim(curr_list=["CAD", "JPY", "GBP", "NZD"], # Run the moving average simulation
                granularity=["H1"], # Granularity
                ma_long=[20,40], # Long moving average
                ma_short=[10], # Short moving average
                filepath="./data"): # Filepath
    ic.LoadInstruments("./data") # Load the instruments from the instruments.json file
    
    for g in granularity: # For each granularity
        for p1 in curr_list: # For each currency
            for p2 in curr_list: # For each currency
                pair = f"{p1}_{p2}" # Create the pair
                if pair in ic.instruments_dict.keys(): # If the pair is in the instruments dictionary
                    analyse_pair(ic.instruments_dict[pair], g, ma_long, ma_short, filepath) # Analyse the pair
        create_ma_res(g) # Create the moving average results





