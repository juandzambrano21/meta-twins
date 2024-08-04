# logger.py

import logging

class Logger:
    """A singleton logger class for consistent logging throughout the application."""
    _instance = None

    def __new__(cls, log_file="system.log"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.init_logger(log_file)
        return cls._instance

    def init_logger(self, log_file):
        self.logger = logging.getLogger("MemGPT")
        self.logger.setLevel(logging.DEBUG)

        # Create handlers for logging to file and console
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        # Set logging levels
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.INFO)

        # Define log format and add to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Attach handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log(self, message, level=logging.INFO):
        """Log messages at the specified logging level."""
        if level == logging.INFO:
            self.logger.info(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.DEBUG:
            self.logger.debug(message)

# Create a global logger instance
logger = Logger().logger
