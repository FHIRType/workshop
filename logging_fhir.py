#Author: Dani Valdovinos

import logging
import datetime as dt
import json
from endpoint import Endpoint
from client import SmartClient
# import time

def initialize_logger(filename):
    """
    Initialize the logger object and configure file handling.
    """

    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger("FHIR")
    
    #do we want to log and append log messages each time it runs the code
    #or do we want to get rid off the old messages and have a fresh log for each day
    # Use 'w' mode to write to a new file each time (overwrite existing)
    # file_handler = logging.FileHandler(filename, mode='w')

    file_handler = logging.FileHandler(filename)

    # file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s: %(filename)s %(levelname)s - %(lineno)d %(message)s",  datefmt="%Y-%m-%d %I:%M:%S %p")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger



    #we could create different filenames to display other information
    #perf_handler = logging.FileHandler(f"performance_{filename}", mode='w')  # Separate file for performance logs
    #perf_handler.setLevel(logging.DEBUG)

    #perf_formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s - Duration: %(duration)s seconds", datefmt="%Y-%m-%d %I:%M:%S %p")
    #perf_handler.setFormatter(perf_formatter)

    #logger.addHandler(perf_handler)
    

def record_log_entries(logger):
    """
    Record sample log entries using the provided logger.
    """
    logger.debug("This is debug")
    logger.info("This is info")
    logger.warning("This is a warning")
    logger.error("There is an error")
    logger.critical("This is critical")


#we can log events within our code such as:
# - logging any errors with connections from endpoints using exceptions or stack traces
# - logging for tracking changes: updates, removing of records
# - logging for performance such as response times for each request, query durations from database

if __name__ == "__main__":
    today = dt.datetime.today()
    filename = f"{today.month:02d}-{today.day:02}-{today.year}.log" #ex: 11-14-2023

    # logging.basicConfig(level=logging.DEBUG)

    #initialize logger
    logger = initialize_logger(filename)

    #record log entries
    record_log_entries(logger)

    #endpoint interaction
    # fhir_endpoint_interaction()