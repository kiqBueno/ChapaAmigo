import os
import logging
import traceback
from app.processPdf import processPdf
from app.interface import runInterface

def main():
    """
    Main function to run the application.
    """
    try:
        runInterface(processPdf)
    except Exception as e:
        logging.error(f"Error running the application: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()