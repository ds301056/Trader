import logging # Python's built-in logging module
import os # Python's built-in os module

LOG_FORMAT = "%(asctime)s %(message)s" # Define the log format
DEFAULT_LEVEL = logging.DEBUG # Define the default log level

class LogWrapper: # Define the LogWrapper class

  PATH = './logs' # Define the path to the logs directory - hard coded  

  def __init__(self, name, mode="w"): # Initialize the LogWrapper object with the name and mode parameters- W overwrites existing log files
    self.create_directory() # Call the create_directory method
    self.filename = f"{LogWrapper.PATH}/{name}.log"
    self.logger = logging.getLogger(name)
    self.logger.setLevel(DEFAULT_LEVEL)

    file_handler = logging.FileHandler(self.filename, mode=mode) # Create a file handler for the log file
    formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S') # Create a formatter for the log messages

    file_handler.setFormatter(formatter) # Set the formatter for the file handler
    self.logger.addHandler(file_handler) # Add the file handler to the logger

    self.logger.info(f"LogWrapper init() {self.filename}")

  def create_directory(self): # Define the create_directory method
    if not os.path.exists(LogWrapper.PATH): # Check if the logs directory does not exist
      os.makedirs(LogWrapper.PATH) # Create the logs directory if it does not exist