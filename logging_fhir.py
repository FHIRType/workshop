import logging
import logging.config
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Load the logging configuration
logging.config.fileConfig("../workshop/logging.ini")

# Get the logger
logger = logging.getLogger('FHIR')

# Dynamically set up TimedRotatingFileHandler with today's date
log_file_name = f"{datetime.now().strftime('%Y-%m-%d')}_fhir.log"
file_handler = TimedRotatingFileHandler(log_file_name, when='midnight', interval=1, backupCount=30, utc=True)
file_handler.setFormatter(logging.Formatter("%(asctime)s: %(filename)s %(levelname)s - %(lineno)d %(message)s", datefmt="%Y-%m-%d %I:%M:%S %p"))
logger.addHandler(file_handler)

# Log some messages
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")