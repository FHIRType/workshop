import logging
import logging.config
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os


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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        package_dir = os.path.dirname(os.path.dirname(script_dir))
        logging_dir = os.path.join(package_dir, "logs/")


        # Dynamically set up TimedRotatingFileHandler with today's date
        log_file_name = f"{logging_dir}{datetime.now().strftime('%Y-%m-%d')}_fhir.log"

        # Create the file
        with open(log_file_name, "w") as file:
            print(log_file_name)


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

        # Log some messages
        # self.logger.debug("debug message")
        # self.logger.info("info message")
        # self.logger.warning("warning message")
        # self.logger.error("error message")
        # self.logger.critical("critical message")
