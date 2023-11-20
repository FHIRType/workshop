import logging
import logging.config
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


# # Load the logging configuration
# logging.config.fileConfig("../src/fhirtypepkg/config/Logging.ini")

# Get the logger
# logger = logging.getLogger('FHIR')

# # Dynamically set up TimedRotatingFileHandler with today's date
# log_file_name = f"{datetime.now().strftime('%Y-%m-%d')}_fhir.log"
# file_handler = TimedRotatingFileHandler(log_file_name, when='midnight', interval=1, backupCount=30, utc=True)
# # file_handler.setFormatter(logging.Formatter("%(asctime)s: %(filename)s %(levelname)s - %(lineno)d %(message)s", datefmt="%Y-%m-%d %I:%M:%S %p"))
# logger.addHandler(file_handler)

# Log some messages
# logger.debug("debug message")
# logger.info("info message")
# logger.warning("warning message")
# logger.error("error message")
# logger.critical("critical message")


class FHIRLogger:
    def __init__(self, config_path):
        # Load the logging configuration
        logging.config.fileConfig(config_path)

        # Initial the logger object
        self.logger = logging.getLogger('FHIR')

        # Dynamically set up TimedRotatingFileHandler with today's date
        log_file_name = f"logs/{datetime.now().strftime('%Y-%m-%d')}_fhir.log"
        file_handler = TimedRotatingFileHandler(log_file_name, when='midnight', interval=1, backupCount=30, utc=True)
        file_handler.setFormatter(logging.Formatter("%(asctime)s: %(filename)s %(levelname)s - %(lineno)d %(message)s", datefmt="%Y-%m-%d %I:%M:%S %p"))
        self.logger.addHandler(file_handler)

        # Log some messages
        # self.logger.debug("debug message")
        # self.logger.info("info message")
        # self.logger.warning("warning message")
        # self.logger.error("error message")
        # self.logger.critical("critical message")


