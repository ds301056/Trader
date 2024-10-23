

from bs4 import BeautifulSoup

from scraping.dailyfx_com import dailyfx_com
from scraping.investing_com import investing_com
from scraping.bloomberg_com import bloomberg_com
from scraping.fx_calender import fx_calender




if __name__ == "__main__":

  #print(dailyfx_com())

  #print(investing_com()) # Call the investing_com_fetch function and print the result

  #data =bloomberg_com() # Call the bloomberg_com function

  #[print(x) for x in data] # Print the result of the bloomberg_com function

  print(fx_calender()) # Call the fx_calender function and print the result