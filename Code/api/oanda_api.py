# Importing necessary libraries
import requests  # Used for making HTTP requests
import pandas as pd  # Used for data manipulation and analysis
import constants.defs as defs  # Importing definitions like API keys and URLs
from dateutil import parser  # Used for parsing dates
from datetime import datetime as dt # Used for date and time operations

# Defining the OandaApi class to encapsulate OANDA API interactions
class OandaApi:

    def __init__(self):
        # Initialize an HTTP session which will be used for all requests
        self.session = requests.Session()
        # Setting default headers for the session, including authorization and content type
        self.session.headers.update({
            "Authorization": f"Bearer {defs.API_KEY}",  # API key for authorization
            "Content-Type": "application/json"  # Data format for requests and responses
        })

    # Method to make requests to the Oanda API
    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None):
        # Constructing the full URL for the API call
        full_url = f"{defs.OANDA_URL}/{url}"

        try:
            response = None
            # Making a GET request if 'get' is specified as the verb
            if verb == "get":
                response = self.session.get(full_url, params=params, data=data, headers=headers)

            # Handling the case where the verb is not recognized
            if response is None:
                return False, {'error': 'verb not found'}

            # Checking if the response status code matches the expected code
            if response.status_code == code:
                return True, response.json()  # Return the JSON response if successful
            else:
                return False, response.json()  # Return the JSON response if unsuccessful
        except Exception as error:
            # Returning False and the error details if an exception occurs
            return False, {'Exception': error}

    # Method to get data from a specific account endpoint
    def get_account_ep(self, ep, data_key):
        # Constructing the URL for the account endpoint
        url = f"accounts/{defs.ACCOUNT_ID}/{ep}"
        # Making the API request using the make_request method
        ok, data = self.make_request(url)

        # Checking if the request was successful and the key is in the response
        if ok == True and data_key in data:
            return data[data_key]  # Return the specific data requested
        else:
            # Print error and return None if unsuccessful
            print("Error: get_account_ep()", data)
            return None

    # Convenience method to get account summary
    def get_account_summary(self):
        # Using get_account_ep method with 'summary' endpoint and 'account' data key
        return self.get_account_ep("summary", "account")

    # Convenience method to get available instruments
    def get_account_instruments(self):
        # Using get_account_ep method with 'instruments' endpoint and 'instruments' data key
        return self.get_account_ep("instruments", "instruments")






    def fetch_candles(self, pair_name, count=10, granularity="H1",
                            price="MBA", date_f=None, date_t=None): # Fetch candles from the OANDA API
        url = f"instruments/{pair_name}/candles" # Construct the URL for the candles endpoint
        params = dict( # Create a dictionary of parameters for the request
            granularity = granularity, # Granularity of the candles
            price = price
        )

        if date_f is not None and date_t is not None: # If date from and date to are specified
            date_format = "%Y-%m-%dT%H:%M:%SZ" # Format for the date and time
            params["from"] = dt.strftime(date_f, date_format) # Set the from parameter to the specified date and time
            params["to"] = dt.strftime(date_t, date_format) # Set the to parameter to the specified date and time
        else:
            params["count"] = count # Set the count parameter to the specified count

        ok, data = self.make_request(url, params=params) # Make the request to the OANDA API
    
        if ok == True and 'candles' in data: # If the request was successful and the candles key is in the response
            return data['candles'] # Return the candles data
        else:
            print("ERROR fetch_candles()", params, data) # Print an error message
            return None # Return None if the request was unsuccessful

    def get_candles_df(self, pair_name, **kwargs): # Get candles as a dataframe **kwargs is a python construct that allows you to pass a variable number of arguments to a function

        data = self.fetch_candles(pair_name, **kwargs) # Fetch the candles data

        if data is None: # If the data is None
            return None # Return None
        if len(data) == 0: # If the length of the data is 0
            return pd.DataFrame() # Return an empty dataframe
        
        prices = ['mid', 'bid', 'ask'] # List of prices
        ohlc = ['o', 'h', 'l', 'c'] # List of OHLC values
        
        final_data = [] # Create an empty list to store the results
        for candle in data: # For each candle in the data
            if candle['complete'] == False: # If the candle is not complete
                continue # Skip to the next candle
            new_dict = {} # Create a new dictionary
            new_dict['time'] = parser.parse(candle['time']) # Parse the time and add it to the dictionary
            new_dict['volume'] = candle['volume'] # Add the volume to the dictionary

            
            for p in prices: # For each price in the list of prices
                if p in candle: # If the price is in the candle
                    for o in ohlc: # For each OHLC value
                        new_dict[f"{p}_{o}"] = float(candle[p][o]) # Add the OHLC value to the dictionary
            final_data.append(new_dict) # Append the new dictionary to the list of results
        df = pd.DataFrame.from_dict(final_data) # Create a dataframe from the list of results
        return df # Return the dataframe

