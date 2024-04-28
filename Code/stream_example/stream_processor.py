import copy # deep copy
import random # random number generator
import threading # threading
import time # time

from stream_example.stream_base import StreamBase # Import the StreamBase class from the stream_base.py file
from queue import Queue # Import the Queue class from the queue module


class PriceProcessor(StreamBase): # Define a PriceProcessor class that extends the threading.Thread class

  def __init__(self, shared_prices, price_lock: threading.Lock, price_events, logname, pair, work_queue: Queue): # Define the __init__ method with the shared_prices, shared_prices_events, shared_prices_lock, and pairs_list arguments
    super().__init__(shared_prices, price_lock, price_events, logname)
    self.pair = pair # Set the pair attribute to the pair argument
    self.work_queue = work_queue # Set the work_queue attribute to the work_queue argument



  def process_price(self): # Define a function called process_price that takes no arguments

    price = None # Set the price to None

    try:

     

      self.price_lock.acquire() # Acquire the price lock
      price = copy.deepcopy(self.shared_prices[self.pair]) # Deep copy the price

    except Exception as error:
      self.log_message(f"CRASH: {error}", error=True) # Log the error
    finally:
      self.price_lock.release() # Release the price lock



    if price is None:
      self.log_message("No price:", error=True) # Log the error
    else:
      self.log_message(f"Found price: {price}")
      #could impliment decisions adn logic here if do something do something put it on queue and work processor will handle 
      time.sleep(random.randint(2, 5)) # Sleep for a random amount of time between 2 and 5 seconds
      self.log_message(f"Done processing price: {price}")
      if random.randint(0,5) == 3: # Randomly decide to add the price to the work queue
        self.log_message(f"Adding work:  {price}")
        self.work_queue.put(price) # Put the price in the work queue

  def run(self): # Define a function called run that takes no arguments

    while True: # Run forever
      self.price_events[self.pair].wait() # Wait for the price event to be set (aka a trigger)
      self.process_price() # Process the price
      self.price_events[self.pair].clear() # Clear the price event

