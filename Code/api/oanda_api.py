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





    def fetch_candles(self, pair_name, count=10, granularity="H1", #fetch_candles method to get candles data
                      price="MBA", date_f=None, date_t=None): #pair_name, count, granularity, price, date_f, date_t are the parameters
        

        url = f"instruments/{pair_name}/candles" #url for the candles endpoint
        params = dict( #parameters for the request
            count = count, #count of candles
            granularity = granularity, #granularity of candles
            price = "MBA" #price of candles
        )

        if date_f is not None and date_t is not None: #if date_f and date_t are not None
            date_format = "%Y-%m-%dT%H:%M:%SZ" #date format
            params["from"] = dt.strftime(date_f, date_format) #from date in the format specified by date_format 
            params["to"] = dt.strftime(date_t, date_format) #to date in the format specified by date_format
        else:
            params["count"] = count #count of candles

        
        ok, data = self.make_request(url, params=params) #make request to the url with the parameters

  
        # Checking if the request was successful and the key is in the response
        if ok == True and 'candles' in data:
            return data['candles']  # Return the specific data requested
        else:
            # Print error and return None if unsuccessful
            print("Error: fetching candles",params,  data)
            return None

    def get_candles_df(self, data):
        if len(data) == 0:
            return pd.DataFrame() #use return pd.DataFrame() not .empty

        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']#keys for looping 


        final_data = []
        for candle in data:
            if candle['complete'] == False:
                continue
            new_dict = {}
            new_dict['time'] = parser.parse(candle['time'])
            new_dict['volume'] = candle['volume']
        
            for p in prices:
                for o in ohlc:
                    new_dict[f"{p}_{o}"]=float(candle[p][o])
            final_data.append(new_dict)
        df = pd.DataFrame.from_dict(final_data)
        return df


