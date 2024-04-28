from queue import Queue # Queue is a thread-safe queue
import threading # Import the threading module
import time # Import the time module

from infrastructure.log_wrapper import LogWrapper # Import the LogWrapper class from the infrastructure/log_wrapper.py file
from models.live_api_price import LiveApiPrice # Import the LiveApiPrice class from the models/live_api_price.py file


class WorkProcessor(threading.Thread):

  def __init__(self, work_queue: Queue):
    super().__init__()
    self.work_queue = work_queue
    self.log = LogWrapper("WorkProcessor")


  def run(self):
      
      while True:
        work: LiveApiPrice = self.work_queue.get() # Get the work from the queue
        self.log.logger.debug(f"New work: {work}") # Log the work
        time.sleep(7) # Sleep for 7 seconds

        


