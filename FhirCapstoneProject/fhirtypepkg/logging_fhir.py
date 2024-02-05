import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


class FHIRLogger:
    def __init__(self, config_path):

        """
        Creates a log file configuration that rotates each day with the filename as the date
        :param config_path: a path to the INI-style configuration file named "Logging.ini"
        """
        # Load the logging configuration
        logging.config.fileConfig(
            config_path
        )  # TODO: Check before loading, raise helpful exception

        # Initial the logger object
        self.logger = logging.getLogger("FHIR")

        # Dynamically set up TimedRotatingFileHandler with today's date
        log_file_name = f"logs/{datetime.now().strftime('%Y-%m-%d')}_fhir.log"

        # Create the file
        tmp = open(log_file_name, "a+")
        tmp.close()

        file_handler = TimedRotatingFileHandler(
            log_file_name, when="midnight", interval=1, backupCount=30, utc=True
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s: %(filename)s %(levelname)s - %(lineno)d %(message)s",
                datefmt="%Y-%m-%d %I:%M:%S %p",
            )
        )
        self.logger.addHandler(file_handler)
