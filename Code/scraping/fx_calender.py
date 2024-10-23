from bs4 import BeautifulSoup # Import the BeautifulSoup class from the bs4 module
from dateutil import parser # Import the parser class from the dateutil module
import pandas as pd # Import the pandas module as pd
import requests # Import the requests module
import cloudscraper  # Import the cloudscraper module
import time # Import the time module
import datetime as dt # Import the datetime module as dt
import random

from db.db import DataDB


pd.set_option("display.max_rows", None) # Set the maximum number of columns to display to None


def get_date(c):  # Define the get_date function
  tr = c.select_one("tr")  # Select the first tr (table row) element in the c object
  ths = list(tr.select("th"))  # Select all th (table header) elements in the tr object
  for th in ths:  # Iterate over the ths list
      if th.has_attr("colspan"):
          date_text = th.get_text().strip() # Get the text of the th element and remove leading/trailing whitespace
          return parser.parse(date_text)  # Parse the date_text string and return the result
  return None  # Return None if no date is found



def get_data_point(key, element): # Define the get_data_point function
  
  for e in['span', 'a']: # Iterate over the list of tags
    d = element.select_one(f"{e}#{key}") # Select the element with the specified tag and id
    if d is not None:
      return d.get_text() # Return the text of the element
    
  return '' # Return an empty string if no element is found


def get_data_for_key(tr, key): # Define the get_data_for_key function
   if tr.has_attr(key): # Check if the key is an attribute of the tr element
      return tr.attrs[key] # Return the value of the key
   return '' # Return an empty string if the key is not found

def get_data_dict(item_date, table_rows): # Define the get_data_dict function

  data = [] # Create an empty list called data

  for tr in table_rows: # Iterate over the table_rows list
      data.append(dict( # Append a dictionary to the data list
          date = item_date, # Set the date key to the item_date value
          country = get_data_for_key(tr, 'data-country'), # Set the country key to the data-country attribute value
          category = get_data_for_key(tr, 'data-category'), # Set the category key to the data-category attribute value
          event = get_data_for_key(tr, 'data-event'), # Set the event key to the data-event attribute value
          symbol = get_data_for_key(tr, 'data-symbol'), # Set the symbol key to the data-symbol attribute value
          actual = get_data_point('actual', tr), # Set the actual key to the result of the get_data_point function
          previous = get_data_point('previous', tr), # Set the previous key to the result of the get_data_point function
          forecast = get_data_point('forecast', tr) # Set the forecast key to the result of the get_data_point function
      ))

  return data # Return the data list




def get_fx_calender(from_date):  # Define the fx_calender function
    # Create a CloudScraper session object, which mimics a browser session that can handle JavaScript challenges
    scraper = cloudscraper.create_scraper()

    fr_d_str = dt.datetime.strftime(from_date, "%Y-%m-%d 00:00:00") # Format the from_date as a string in the format YYYY-MM-DD
    
    to_date = from_date + dt.timedelta(days=6) # Add 6 days to the from_date
    to_d_str = dt.datetime.strftime(to_date, "%Y-%m-%d 00:00:00")
    # Define headers if needed (CloudScraper already includes a user-agent)
    headers = {
        "Cookie": "calendar-importance=3; cal-custom-range={fr_d_str}|{to_d_str}; TEServer=TEIIS3; cal-timezone-offset=0;"
    }

    # Send a GET request using the CloudScraper session
    resp = scraper.get("https://tradingeconomics.com/calendar", headers=headers)

    # Create a BeautifulSoup object from the response content
    soup = BeautifulSoup(resp.content, 'html.parser')

    table = soup.select_one("table#calendar") # Select the table element with the id calendar

    last_header_date = None # Create a variable called last_header_date and set it to None    
    trs = {} # Create an empty dictionary called trs

    final_data = [] # Create an empty list called final_data




    for c in table.children: # Iterate over the children of the table element
        if c.name == 'thead': # Check if the element is a thead element
            if 'class' in c.attrs and 'hidden-head' in c.attrs['class']: # Check if the element has a hidden-head class
                continue
            last_header_date = get_date(c) # Set the last_header_date variable to the result of the get_date function
            trs[last_header_date] = [] # Add a new key-value pair to the trs dictionary
        elif c.name == 'tr': # Check if the element is a tr element
            trs[last_header_date].append(c) # Append the tr element to the list in the trs dictionary

    for item_date, table_rows in trs.items(): # Iterate over the items in the trs dictionary
      final_data += get_data_dict(item_date, table_rows) # Add the result of the get_data_dict function to the final_data list
        
    #[print(x) for x in final_data] # Print the final_data list
    return final_data # Return the final_data list

def fx_calender(): # Define the fx_calender function
   
   #final_data = [] # Create an empty list called final_data

   start = parser.parse("2021-05-03T00:00:00Z") # Parse the start date string
   end = parser.parse("2022-03-25T00:00:00Z") # Parse the end date string

   database = DataDB() # Create a DataDB object
   
   while start < end:
     data = get_fx_calender(start) # Add the result of the get_fx_calender function to the final_data list
     print(start, len(data)) # Print the start date and the length of the data list
     database.add_many(DataDB.CALENDAR_COLL, data) # Add the data list to the database
     start =start + dt.timedelta(days=7) # Increment the start date by one day
     time.sleep(random.randint(1,4)) # Pause for 1-4 seconds to look human

   #print(pd.DataFrame.from_dict(final_data)) # Print the final_data list as a DataFrame
