#oanda api
# Importing necessary libraries
import requests  # Used for making HTTP requests
import pandas as pd  # Used for data manipulation and analysis
import json # Used for working with JSON data
import constants.defs as defs  # Importing definitions like API keys and URLs

from models.api_price import Api_Price # Import the ApiPrice class from the models/api_price.py file
from dateutil import parser  # Used for parsing dates
from datetime import datetime as dt # Used for date and time operations
from infrastructure.instrument_collection import instrumentCollection as ic # Import the instrumentCollection instance from the infrastructure/instrument_collection.py file
from models.open_trade import OpenTrade # Import the OpenTrade class from the models/open_trade.py file

# Defining the OandaApi class to encapsulate OANDA API interactions
class OandaApi:

    def __init__(self):
        # Initialize an HTTP session which will be used for all requests
        self.session = requests.Session()
        # Setting default headers for the session, including authorization and content type
        self.session.headers.update(defs.SECURE_HEADER)

    # Method to make requests to the Oanda API
    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None):
        # Constructing the full URL for the API call
        full_url = f"{defs.OANDA_URL}/{url}"
        #print(f"Making {verb.upper()} request to: {full_url}")  # Displaying the full URL being accessed

        if params:
            #print(f"With parameters: {params}")  # Log the parameters if present
            pass

        if data is not None:  # If data is not None
            data = json.dumps(data)  # Convert the data to JSON format if it is not None
            #print(f"With payload: {data}")  # Log the data being sent

        try:
            response = None
            if verb == "get":
                response = self.session.get(full_url, params=params, headers=headers)
            if verb == "post":
                response = self.session.post(full_url, data=data, headers=headers)
            if verb == "put":
                response = self.session.put(full_url, data=data, headers=headers)


            if response is None:
                print("No response received.")
                return False, {'error': 'verb not found'}

            # Logging the response status and data
            #print(f"Response Status: {response.status_code}")
            #print(f"Response Data: {response.text}")  # Logs the raw response text

            if response.status_code == code:
                return True, response.json()  # Return the JSON response if successful
            else:
                return False, response.json()  # Return the JSON response if unsuccessful

        except Exception as error:
            # Log the error if an exception occurs
            print(f"Exception during API call: {error}")
            return False, {'Exception': str(error)}


    # Method to get data from a specific account endpoint
    def get_account_ep(self, ep, data_key):
        # Constructing the URL for the account endpoint
        url = f"accounts/{defs.ACCOUNT_ID}/{ep}"
        # Making the API request using the make_request method
        ok, data = self.make_request(url)

        # Log the entire JSON response to inspect it
        #print("Full API Response:", json.dumps(data, indent=4)) #debugging

        # Checking if the request was successful and the key is in the response
        if ok and data_key in data:
            return data[data_key]  # Return the specific data requested
        else:
            # Print error and return None if unsuccessful or data_key not found
            print("ERROR: get_account_ep() - Data key not found or error in response", data)
            return None


    # Convenience method to get account summary
    def get_account_summary(self):
        # Using get_account_ep method with 'summary' endpoint and 'account' data key
        return self.get_account_ep("summary", "account")

    # Convenience method to get available instruments
    def get_account_instruments(self):
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

    def get_candles_df(self, pair_name, **kwargs): # Get the candles data as a pandas DataFrame

        data = self.fetch_candles(pair_name, **kwargs) # Fetch the candles data from the OANDA API

        if data is None: # Check if there is no data
            return None # Return None if there is no data
        if len(data) == 0: # Check if there is no data
            return pd.DataFrame() # Return an empty DataFrame if there is no data
        
        prices = ['mid', 'bid', 'ask'] # Mid, bid, and ask prices 
        ohlc = ['o', 'h', 'l', 'c'] # Open, high, low, close prices
        
        final_data = [] # Create an empty list to store the candles data
        for candle in data: # Iterate over the candles data
            if candle['complete'] == False: # Check if the candle is complete
                continue
            new_dict = {} # Create a new dictionary to store the candle data
            new_dict['time'] = parser.parse(candle['time']) # Parse the time data and add it to the new dictionary
            new_dict['volume'] = candle['volume'] # Add the volume data to the new dictionary
            for p in prices: # Iterate over the mid, bid, and ask prices
                if p in candle: # Check if the price data is present in the candle
                    for o in ohlc: # Iterate over the open, high, low, and close prices
                        new_dict[f"{p}_{o}"] = float(candle[p][o]) # Add the open, high, low, and close prices to the new dictionary
            final_data.append(new_dict) # Append the new dictionary to the final data list
        df = pd.DataFrame.from_dict(final_data) # Create a pandas DataFrame from the candles data
        return df # Return the candles data as a pandas DataFrame



    def last_complete_candle(self, pair_name, granularity):
        df = self.get_candles_df(pair_name, granularity=granularity, count=10) # Get the last two candles
        if df.shape[0] == 0:
            return None
        return df.iloc[-1].time # Return the last candle

    def place_trade(self, pair_name: str, units: float, direction: int,
                        stop_loss: float=None, take_profit: float=None):
      
        url = f"accounts/{defs.ACCOUNT_ID}/orders" # Construct the URL for the orders endpoint

        instrument = ic.instruments_dict[pair_name] # Get the instrument ID for the specified pair
        units = round(units, instrument.tradeUnitsPrecision) # Round the units to the trade units precision

        if direction == defs.SELL:
            units = units * -1 # If the direction is sell, make the units negative


        data = dict(
            order =dict(
                units=str(units), # Number of units to trade
                instrument =pair_name, # Instrument to trade
                type="MARKET" # Market order type
            )
        )

        if stop_loss is not None:
            sld = dict(price=str(round(stop_loss, instrument.displayPrecision))) # Set the stop loss price
            data['order']['stopLossOnFill'] = sld # Add the stop loss to the order data to stop loss dictionary

        if take_profit is not None:
            tpd = dict(price=str(round(take_profit, int(instrument.displayPrecision)))) # Set the take profit price
            data['order']['takeProfitOnFill'] = tpd # Add the take profit to the order data to take profit dictionary

        #print(data)

        ok, response = self.make_request(url, verb="post", data=data, code=201) # Make the request to the OANDA API

        #print(ok, response)

        #get open trade id
        if ok == True and 'orderFillTransaction' in response: # If the request was successful and the orderFillTransaction key is in the response
            return response['orderFillTransaction']['id'] # Return the order fill transaction data
        else:
            return None # Return None if the request was unsuccessful
        
    def close_trade(self, trade_id): # Close a trade based on the trade ID
        url = f"accounts/{defs.ACCOUNT_ID}/trades/{trade_id}/close"
        ok, _ = self.make_request(url, verb="put", code=200) # Make the request to the OANDA API

        if ok == True: 
            print(f"closed {trade_id} successfully") # Print a success message if the trade was closed successfully
        else:
            print(f"failed to close {trade_id}") # Print an error message if the trade failed to close

        return ok # Return the result of the request
    
    def get_open_trade(self, trade_id): # Get the details of an open trade based on the trade ID
        url = f"accounts/{defs.ACCOUNT_ID}/trades/{trade_id}" # Construct the URL for the trades endpoint
        ok, response = self.make_request(url) # Make the request to the OANDA API
        
        if ok == True and 'trade' in response:
            return OpenTrade(response['trade']) # Return the trade data as an OpenTrade object
        
    def get_open_trades(self):
        url = f"accounts/{defs.ACCOUNT_ID}/openTrades" # Construct the URL for the trades endpoint
        ok, response = self.make_request(url) # Make the request to the OANDA API
        
        if ok == True and 'trades' in response: # If the request was successful and the trades key is in the response
            return [OpenTrade(x) for x in response['trades']] # Return the trade data as a list of OpenTrade objects
        

    def get_prices(self, instruments_list):
        url = f"accounts/{defs.ACCOUNT_ID}/pricing" # Construct the URL for the pricing endpoint

        # Create a dictionary of parameters for the request
        params = dict(
            instruments=','.join(instruments_list),
            includeHomeConversions=True
            ) 
        
        ok, response = self.make_request(url, params=params) # Make the request to the OANDA API

        if ok == True and 'prices' in response and 'homeConversions' in response: # If the request was successful and the prices and homeConversions keys are in the response
            return [Api_Price(x, response['homeConversions']) for x in response['prices']] # Return the price data as a list of OpenTrade objects
        
        return None # Return None if the request was unsuccessful