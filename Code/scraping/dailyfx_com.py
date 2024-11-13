from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML
import pandas as pd  # Import pandas for DataFrame operations
import requests  # Import requests to make HTTP requests

def dailyfx_com():
    resp = requests.get('https://www.dailyfx.com/sentiment')  # Make a GET request to the website
    
    soup = BeautifulSoup(resp.content, 'html.parser')  # Parse the HTML content using BeautifulSoup
    rows = soup.select(".dfx-technicalSentimentCard")  # Select all elements with the class

    pair_data = [] # Initialize an empty list to store the data


    for r in rows: # Iterate through the selected elements
        card = r.select_one(".dfx-technicalSentimentCard__pairAndSignal") # Select the element with the class
        change_values = r.select(".dfx-technicalSentimentCard__changeValue") # Select all elements with the class
        pair_data.append(dict(
            pair=card.select_one('a').get_text().replace("/", "_").strip("\n"),   
            sentiment=card.select_one('span').get_text().strip("\n"),   
            longs_d=change_values[0].get_text().strip("\n"),
            shorts_d=change_values[1].get_text().strip("\n"),
            longs_w=change_values[3].get_text().strip("\n"),
            shorts_w=change_values[4].get_text().strip("\n")

        ))

    return pd.DataFrame.from_dict(pair_data)  # Return the data as a pandas DataFrame

        



        
            
