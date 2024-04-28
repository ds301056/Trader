import json # Import the json module
import threading  # Import the threading module
import time

from queue import Queue # Import the Queue class from the queue module
from stream_example.stream_worker import WorkProcessor
from stream_example.stream_processor import PriceProcessor # Import the PriceProcessor class
from stream_example.stream_prices import PriceStreamer # Import the time module

def load_settings(): # Define the load_settings function
  with open("./bot/settings.json", "r") as f: # Open the settings.json file in read mode
      return json.loads(f.read()) # Return the JSON data from the file

def run_streamer(): # Define the run_streamer function

  settings = load_settings() # Load the settings

  shared_prices = {} # Create an empty dictionary for shared prices
  shared_prices_events = {} # Create an empty dictionary for shared prices events
  shared_prices_lock = threading.Lock() # Create a lock for the shared prices
  work_queue = Queue() # Create a queue for the work

  for p in settings['pairs'].keys():
     shared_prices_events[p] = threading.Event() # Create an event for each pair
     shared_prices[p] = {} # Create an empty dictionary for each pair

  threads = [] # Create an empty list for threads

  price_stream_t = PriceStreamer(shared_prices, shared_prices_lock, shared_prices_events) # Create a thread for the price streamer
  price_stream_t.daemon = True # Set the daemon attribute of the price streamer thread to True
  threads.append(price_stream_t) # Append the thread to the threads list
  price_stream_t.start() # Start the thread

  
  worker_t = WorkProcessor(work_queue) # Create a thread for the price streamer
  worker_t.daemon = True # Set the daemon attribute of the price streamer thread to True
  threads.append(worker_t) # Append the thread to the threads list
  worker_t.start() # Start the thread


  for p in settings['pairs'].keys():
    processing_t = PriceProcessor(shared_prices, shared_prices_lock, shared_prices_events,
                                  f"PriceProcessor_{p}", p, work_queue) # Create a thread for the price processor

    processing_t.daemon = True # Set the daemon attribute of the price processor thread to True
    threads.append(processing_t) # Append the thread to the threads list
    processing_t.start() # Start the thread


  #for t in threads: # Iterate over the threads
    # t.join() # Join the thread

  try: # use sleep as a work-around for signial init (python packages) windows issue
    while True:
      time.sleep(0.5)
  except KeyboardInterrupt:
     print("Keyboard interrupt detected")
    
     

  print("ALL DONE")
