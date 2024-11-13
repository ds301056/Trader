from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML
import pandas as pd  # Import pandas for DataFrame operations
import requests  # Import requests to make HTTP requests
import datetime as dt # Import datetime for date operations
import time # Import time for time operations
import constants.defs as defs # Import the constants from the defs.py file



data_keys = [ # Define a list of keys for the data
  'pair_name', 
  'ti_buy', 
  'ti_sell', 
  'ma_buy', 
  'ma_sell', 
  'S1', 
  'S2', 
  'S3', 
  'pivot', 
  'R1', 
  'R2', 
  'R3', 
  'percent_bullish', 
  'percent_bearish'
]



def get_data_object(text_list, pair_id, time_frame): # Define a function to get the data object from the text list
  data = {} # Initialize an empty dictionary
  data['pair_id'] = pair_id # Set the pair ID in the data dictionary
  data['time_frame'] = time_frame # Set the time frame in the data dictionary 
  data['updated'] = dt.datetime.utcnow() # Set the updated time in the data dictionary

  for item in text_list: # Iterate over the items in the text list
    temp_item = item.split("=") # Split the item by the equals sign
    if len(temp_item) == 2 and temp_item[0] in data_keys: # Check if the length of the item is 2 and the first element is in the data keys
      data[temp_item[0]] = temp_item[1] # Add the item to the data dictionary

    # format the data returned
    if 'pair_name' in data: # Check if the pair_name key is in the data dictionary
      data['pair_name'] = data['pair_name'].replace("/", "_") # Replace the forward slash with an underscore

  return data


def investing_com_fetch(pair_id, time_frame): # Define a function to scrape data from investing.com

  params = dict( # Define a dictionary with the parameters for the request
    action='get_studies',
    pair_ID=pair_id, # Set the pair ID
    time_frame=time_frame # Set the time frame
  )

  resp = requests.get("https://www.investing.com/common/technical_studies/technical_studies_data.php",
                      params=params) # Make a GET request to the website
  

  #print(resp.content) # Print the content of the response
  #print(resp.status_code) # Print the status code of the response

  text = resp.content.decode('utf-8') # Decode the content of the response

  index_start = text.index("pair_name=") # Find the index of the start of the data
  index_end = text.index("*;*quote_link") # Find the index of the end of the data

  data_str = text[index_start:index_end] # Print the data

  split_data_str = data_str.split('*;*') # Split the data into a list of strings

  return get_data_object(data_str.split('*;*'), pair_id, time_frame) # Print the data object

def investing_com():
  data = [] # Initialize an empty list for the data
  for pair_id in range (1, 12): # Iterate over the pair IDs
    for time_frame in [3600, 86400]: # Iterate over the time frames
      print(pair_id, time_frame)
      data.append(investing_com_fetch(pair_id, time_frame)) # Append the data object to the data list
      time.sleep(0.5) # Sleep for 0.5 seconds to not smash website server 

  return pd.DataFrame.from_dict(data) # Return the data as a DataFrame


def get_pair(pair_name, tf): # Define a function to get the pair and timeframe

  if tf not in defs.TFS: # Check if the time frame is not in the time frames
    tf = defs.TFS['H1']
  else: 
    tf = defs.TFS[tf]

  if pair_name in defs.INVESTING_COM_PAIRS: # Check if the pair name is in the investing.com pairs
    pair_id = defs.INVESTING_COM_PAIRS[pair_name]['pair_id'] # Get the pair ID from the investing.com pairs
    return investing_com_fetch(pair_id, tf) # Return the data object
