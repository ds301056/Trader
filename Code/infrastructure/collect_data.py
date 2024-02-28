import pandas as pd # Import the pandas library for data manipulation and analysis.
import datetime as dt # Import the datetime module for handling dates and times.
from dateutil import parser # Import the parser module from dateutil to parse strings into datetime objects.

# Import the InstrumentCollection class from a local module to manage collections of financial instruments.
from infrastructure.instrument_collection import InstrumentCollection
# Import the OandaApi class from a local module to interact with the OANDA API for financial data.
from api.oanda_api import OandaApi

CANDLE_COUNT = 3000 # Define the constant for the number of candles to fetch, which dictates the size of the data to be retrieved.

# Define a dictionary that maps candle granularity to the number of minutes it represents. This is used to calculate time steps.
INCREMENTS = { 
    'M5' : 5 * CANDLE_COUNT, # Multiply the number of minutes by the number of candles to fetch.
    'H1' : 60 * CANDLE_COUNT, # Multiply the number of minutes by the number of candles to fetch.
    'H4' : 240 * CANDLE_COUNT # Multiply the number of minutes by the number of candles to fetch.
}

def save_file(final_df: pd.DataFrame, file_prefix, granularity, pair):
    """
    Saves the final DataFrame to a pickle file and prints a summary.

    Parameters:
    - final_df: The DataFrame to be saved.
    - file_prefix: Prefix for the filename, indicating the file's location or purpose.
    - granularity: The time granularity of the data.
    - pair: The currency pair the data is for.
    """
    filename = f"{file_prefix}{pair}_{granularity}.pkl" # Format the filename using the provided parameters.

    # Clean the DataFrame by dropping duplicate entries based on the 'time' column, sorting by time, and resetting the index.
    final_df.drop_duplicates(subset=['time'], inplace=True)
    final_df.sort_values(by='time', inplace=True)
    final_df.reset_index(drop=True, inplace=True)
    
    final_df.to_pickle(filename) # Save the DataFrame to a pickle file using the formatted filename.

    # Print a summary message indicating the pair, granularity, time range, and number of candles saved.
    s1 = f"*** {pair} {granularity} {final_df.time.min()} {final_df.time.max()}"
    print(f"*** {s1} --> {final_df.shape[0]} candles ***")

def fetch_candles(pair, granularity, date_f: dt.datetime, date_t: dt.datetime, api: OandaApi):
    """
    Attempts to fetch candle data from the OANDA API.

    Parameters:
    - pair: The currency pair to fetch data for.
    - granularity: The time granularity of the data.
    - date_f: The start date for the data fetch.
    - date_t: The end date for the data fetch.
    - api: An instance of the OandaApi class to use for fetching the data.

    Returns:
    - A DataFrame containing the fetched candle data, or None if the fetch fails.
    """
    attempts = 0 # Initialize the attempt counter to 0.

    # Attempt to fetch the candle data up to 3 times.
    while attempts < 3:
        # Use the OandaApi instance to fetch the candle data as a DataFrame.
        candles_df = api.get_candles_df(
            pair,
            granularity=granularity,
            date_f=date_f,
            date_t=date_t
        )

        # If the DataFrame is not None (indicating a successful fetch), break the loop and return the data.
        if candles_df is not None:
            break

        attempts += 1 # Increment the attempt counter if the fetch was unsuccessful.

    # After exiting the loop, check if the DataFrame is both not None and not empty.
    if candles_df is not None and not candles_df.empty:
        return candles_df # Return the DataFrame if it contains data.
    else:
        return None # Return None if the DataFrame is either None or empty.

def collect_data(pair, granularity, date_f, date_t, file_prefix, api: OandaApi):
    """
    Collects candle data over a specified period and granularity, then saves it.

    Parameters:
    - pair: The currency pair to collect data for.
    - granularity: The time granularity of the data.
    - date_f: The start date (in string format) for the data collection.
    - date_t: The end date (in string format) for the data collection.
    - file_prefix: Prefix for the filename, indicating the file's location or purpose.
    - api: An instance of the OandaApi class to use for fetching the data.
    """
    time_step = INCREMENTS[granularity] # Determine the time step based on the granularity.

    end_date = parser.parse(date_t) # Parse the end date string into a datetime object.
    from_date = parser.parse(date_f) # Parse the start date string into a datetime object.

    candle_dfs = [] # Initialize an empty list to hold the candle data DataFrames.

    to_date = from_date # Set the initial 'to date' to the start date.

    # Continue fetching data in increments until reaching the end date.
    while to_date < end_date:
        # Calculate the 'to date' for the current fetch increment.
        to_date = from_date + dt.timedelta(minutes=time_step)
        # If the calculated 'to date' exceeds the end date, adjust it to match the end date.
        if to_date > end_date:
            to_date = end_date

        # Fetch the candle data for the current increment.
        candles = fetch_candles(
            pair,
            granularity,
            from_date,
            to_date,
            api
        )

        # If data was successfully fetched, add it to the list of DataFrames.
        if candles is not None:
            candle_dfs.append(candles)
            # Print a message indicating the successful data fetch for the current increment.
            print(f"{pair} {granularity} {from_date} {to_date} --> {candles.shape[0]} candles loaded")
        else:
            # Print a message indicating that no data was fetched for the current increment.
            print(f"{pair} {granularity} {from_date} {to_date} --> NO CANDLES")

        from_date = to_date # Update the 'from date' for the next increment.

    # If any data was fetched and stored in the list of DataFrames, concatenate them and save the result.
    if len(candle_dfs) > 0:
        final_df = pd.concat(candle_dfs) # Concatenate the list of DataFrames into a single DataFrame.
        save_file(final_df, file_prefix, granularity, pair) # Save the concatenated DataFrame.
    else:
        # Print a message indicating that no data was fetched or saved.
        print(f"{pair} {granularity} --> NO DATA SAVED!")

def run_collection(ic: InstrumentCollection, api: OandaApi):
    """
    Runs the data collection process for a set of currency pairs and a specific granularity.

    Parameters:
    - ic: An instance of InstrumentCollection containing the currency pairs to be processed.
    - api: An instance of the OandaApi class to use for fetching the data.
    """
    our_curr = ["EUR", "GBP", "AUD"] # Define a list of currencies for which to collect data.

    # Iterate over all combinations of the specified currencies to form currency pairs.
    for p1 in our_curr:
        for p2 in our_curr:
            pair = f"{p1}_{p2}" # Form the currency pair string.
            # Check if the formed pair is present in the instruments dictionary of the InstrumentCollection instance.
            if pair in ic.instruments_dict.keys():
                # For each specified granularity, collect data for the currency pair.
                for granularity in ["M5"]: # Here, we're only collecting data at 1-hour granularity.
                    # Print the currency pair and granularity being processed.
                    print(pair, granularity)
                    # Call the function to collect and save data for the currency pair and granularity.
                    collect_data(
                        pair,
                        granularity,
                        "2016-01-07T00:00:00Z", # Define the start date for data collection.
                        "2021-12-31T00:00:00Z", # Define the end date for data collection.
                        "./data", # Define the file prefix (file location).
                        api # Pass the OandaApi instance for data fetching.
                    )
