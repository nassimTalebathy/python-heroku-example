# File that contains the logger for the application. 
# The logging should be the most verbose level, and include a timestamp in South African Time. 
# Also write to a file in the root directory called "app.log.txt"
import logging
import os
from datetime import datetime, timezone, timedelta

# Set up the logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

if len(logger.handlers) == 0:
    # Create a formatter with a custom format
    log_format = "%(asctime)s [SA] %(levelname)s: %(message)s"
    formatter = logging.Formatter(log_format)
    # Create a file handler and set the formatter
    log_file_path = os.path.join(os.path.dirname(__file__), "app.log.txt")
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    # Stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    # Set the time zone to South African Time (UTC+2)
    sast = timezone(timedelta(hours=2))
    logging.Formatter.converter = lambda *args: datetime.now(sast).timetuple()


