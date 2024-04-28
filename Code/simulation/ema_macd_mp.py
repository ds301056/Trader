from multiprocessing import Process # Import Process from multiprocessing module


import pandas as pd  # Import pandas library for data manipulation and analysis
from dateutil import parser  # Import parser from dateutil to parse dates
from technicals.indicators import MACD  # Import MACD function from a custom library for financial technical indicators
from simulation.guru_tester import GuruTester  # Import GuruTester, a custom class for testing trading strategies
from infrastructure.instrument_collection import InstrumentCollection  # Import a custom class for managing collections of financial instruments

# Constants for buy, sell, and no action signals
BUY = 1
SELL = -1
NONE = 0

def apply_signal(row):
    # Define a function to determine buy or sell signals based on EMA and mid_l (likely mean lower price) criteria
    if row.direction == BUY and row.mid_l > row.EMA:
        return BUY
    if row.direction == SELL and row.mid_h < row.EMA:
        return SELL
    return NONE   

def apply_cross(row):
    # Define a function to determine buy or sell signals based on MACD crossovers
    if row.macd_delta > 0  and row.macd_delta_prev < 0:
        return BUY
    if row.macd_delta < 0  and row.macd_delta_prev > 0:
        return SELL
    return NONE  

def prepare_data(df: pd.DataFrame, slow, fast, signal, ema):
    # Prepare the data by calculating MACD, MACD delta, direction, and EMA
    df_an = df.copy()  # Create a copy of the dataframe to avoid modifying the original
    df_an = MACD(df_an, n_slow=slow, n_fast=fast, n_signal=signal)  # Calculate MACD values
    df_an['macd_delta'] = df_an.MACD - df_an.SIGNAL  # Compute delta between MACD and signal line
    df_an['macd_delta_prev'] = df_an.macd_delta.shift(1)  # Shift the MACD delta to get previous values
    df_an['direction'] = df_an.apply(apply_cross, axis=1)  # Apply the cross function to determine the direction
    df_an['EMA'] = df_an.mid_c.ewm(span=ema, min_periods=ema).mean()  # Calculate Exponential Moving Average (EMA)
    df_an.dropna(inplace=True)  # Remove rows with NaN values
    df_an.reset_index(drop=True, inplace=True)  # Reset index after dropping rows
    return df_an

def load_data(pair, time_d=1):
    # Function to load data for a given pair and time duration
    start = parser.parse("2020-11-01T00:00:00Z")  # Parse the start date
    end = parser.parse("2021-01-01T00:00:00Z")  # Parse the end date

    df = pd.read_pickle(f"./data/{pair}_H{time_d}.pkl")  # Load hourly data for the pair
    df_m5 = pd.read_pickle(f"./data/{pair}_M5.pkl")  # Load data for every 5 minutes for the pair

    df = df[(df.time>=start)&(df.time<end)]  # Filter data within the specified time range
    df_m5 = df_m5[(df_m5.time>=start)&(df_m5.time<end)]  # Filter data within the specified time range

    df.reset_index(drop=True, inplace=True)  # Reset index after filtering
    df_m5.reset_index(drop=True, inplace=True)  # Reset index after filtering

    return df, df_m5  # Return both dataframes

def simulate_params(pair, df, df_m5, slow, fast, signal, ema, time_d):
    # Simulate trading parameters and perform the trading test
    prepped_df = prepare_data(df, slow, fast, signal, ema)  # Prepare data for simulation
    gt = GuruTester(
        prepped_df,
        apply_signal,
        df_m5,
        use_spread=True,
        time_d=time_d
    )  # Initialize GuruTester with the prepared data and simulation settings
    gt.run_test()  # Run the trading test

    gt.df_results['slow'] = slow  # Record the slow parameter in results
    gt.df_results['fast'] = fast  # Record the fast parameter in results
    gt.df_results['signal'] = signal  # Record the signal parameter in results
    gt.df_results['ema'] = ema  # Record the ema parameter in results
    gt.df_results['pair'] = pair  # Record the pair parameter in results

    return gt.df_results  # Return the results dataframe

def run_pair(pair):
    # Function to run simulations for a specific currency pair
    time_d = 4  # Set the time duration for the data

    df, df_m5 = load_data(pair, time_d=time_d)  # Load data for the pair

    results = []  # Initialize a list to store results
    trades = []  # Initialize a list to store trade data

    print("\n--> Running", pair)  # Print the pair being processed

    # Nested loops to test different combinations of parameters
    for slow in [26,52]:
        for fast in [12,18]:
            if slow <= fast:  # Ensure slow is greater than fast
                continue
            for signal in [9,12]:
                for ema in [50,100]:
                    sim_res_df = simulate_params(pair, df, df_m5, slow, fast, signal, ema, time_d)
                    r = sim_res_df.result.sum()
                    trades.append(sim_res_df)
                    print(f"--> {pair} {slow} {fast} {ema} {signal} {r}")
                    results.append(dict(
                        pair=pair,
                        slow=slow,
                        fast=fast,
                        ema=ema,
                        result=r,
                        signal=signal
                    ))
    pd.concat(trades).to_pickle(f"./exploration/macd_ema/trades/macd_ema_trades_{pair}.pkl")  # Save trade data to pickle
    return pd.DataFrame.from_dict(results)  # Return results as a dataframe




def run_process(pair): # Function to run a process
    print(f"Process {pair} started") # Function to run a process
    results = run_pair(pair)  # Run simulation for the pair
    results.to_pickle(f"./exploration/macd_ema/macd_ema_res_{pair}.pkl")  # Save results to pickle
    print(f"Process {pair} ended") # Function to run a process



def get_sim_pairs(l_curr, ic: InstrumentCollection): # Function to get valid currency pairs for simulation
    pairs = [] # Create an empty list to store pairs

    for p1 in l_curr: # Loop over the currencies
        for p2 in l_curr: # Loop over the currencies
            pair = f"{p1}_{p2}" # Create a currency pair
            if pair in ic.instruments_dict.keys(): # Check if the pair is valid
                pairs.append(pair) # Append the pair to the list of pairs
    return pairs # Return the list of pairs
    

def run_ema_macd(ic: InstrumentCollection): # Function to run multiple processes
    
    pairs = get_sim_pairs (['USD', 'GBP', 'JPY', 'NZD', 'AUD', 'CAD'], ic)# Get valid currency pairs for simulation


    limit = 4 # Set the limit of processes to run determined by cpu cores available
    current =0 # Set the current index for processes running

    while current < len(pairs):

    
        processes = [] # Create an empty list to store processes
        todo = len(pairs) - current # Calculate the number of processes to run
        if todo < limit: # If the number of processes to run is less than the limit
            limit = todo # Set the limit to the number of processes to run

        for _ in range(limit): # Loop 4 times
            processes.append(Process(target=run_process, args=(pairs[current],) )) # Create a process with a target function and arguments
            current += 1

        for p in processes: # Loop over processes
            p.start() # Start the process

        for p in processes: # Loop over processes
            p.join() # Wait for the process to finish before going to the next process

    print("All processes finished") # Print a message when all processes are finished