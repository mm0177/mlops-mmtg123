import sys
import traceback

def log_exception(exc_type, exc_value, exc_tb):
    """
    This function logs exception details like message, line number, and traceback.
    """
    # Get the line number where the error occurred
    line_number = exc_tb.tb_lineno

    # Get the traceback details as a string
    tb_message = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))

    # Display the error message along with the traceback
    print(f"Exception occurred at line {line_number}:")
    print(f"Message: {str(exc_value)}")
    print(f"Traceback:{tb_message}")

# Set the custom exception hook to use the above function
sys.excepthook = log_exception

# Test code that triggers an exception
def risky_function():
    return 1 / 0  # This will raise a ZeroDivisionError

risky_function()
