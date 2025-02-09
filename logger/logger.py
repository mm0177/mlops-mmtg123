import logging

# Configure logging
logging.basicConfig(
    filename='application.log',   # Log file name
    level=logging.DEBUG,          # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format: time, level, and message
    datefmt='%Y-%m-%d %H:%M:%S'    # Date format (Year-Month-Day Hour:Minute:Second)
)
logger = logging.getLogger()

# Example usage of logging
