import logging
import os

class MainLogHandler:
    LOG_PATH = './logs'
    LOG_FILE = 'main_log_history.log'
    LOG_FORMAT = "%(asctime)s %(message)s"
    DEFAULT_LEVEL = logging.DEBUG

    def __init__(self):
        self.create_log_directory()
        self.setup_logging()

    def create_log_directory(self):
        # Create the log directory if it does not exist
        if not os.path.exists(MainLogHandler.LOG_PATH):
            os.makedirs(MainLogHandler.LOG_PATH)

    def setup_logging(self):
        # Set up the logger specifically for the main log
        self.logger = logging.getLogger('MainLogger')
        self.logger.setLevel(MainLogHandler.DEFAULT_LEVEL)

        log_filename = os.path.join(MainLogHandler.LOG_PATH, MainLogHandler.LOG_FILE)

        # Ensure the logger does not duplicate logs
        if not self.logger.handlers:
            # Create file handler with append mode
            file_handler = logging.FileHandler(log_filename, mode='a')
            formatter = logging.Formatter(MainLogHandler.LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def log(self, message):
        # Log a message
        self.logger.info(message)