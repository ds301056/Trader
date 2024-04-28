from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML
import pandas as pd  # Import pandas for DataFrame operations
import requests  # Import requests to make HTTP requests

def dailyfx_com():
    resp = requests.get('https://www.dailyfx.com/sentiment')  # Make a GET request to the website
    # Uncomment below lines to debug the HTTP response content and status
    # print(resp.content)
    # print(resp.status_code)

    soup = BeautifulSoup(resp.content, 'html.parser')  # Parse the HTML content using BeautifulSoup
    # Uncomment below line to debug the parsed HTML structure
    # print(soup)

    rows = soup.select(".dfx-technicalSentimentCard")  # Select all elements with the class

    for r in rows:
        card = r.select_one(".dfx-technicalSentimentCard__pairAndSignal")
        if card:
            a_tag = card.select_one('a')
            if a_tag:
                print(a_tag.get_text().replace("/", "_"))  # Print the text of the <a> tag, replacing "/" with "_"
            else:
                print("No link found in the card")

            span_tag = card.select_one('span')
            if span_tag:
                print(span_tag.get_text())  # Print the text of the <span> tag
            else:
                print("No span found in the card")



            
