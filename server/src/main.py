"""
This module controls the flow of the program.
It reads the user input, scrapes the ratings and review counts for the given restaurant, and prints the results.
Author: Noah Landis
"""
import logging
import os
import sys

import bugsnag
from bugsnag.handlers import BugsnagHandler
from dotenv import load_dotenv

from client.cli.src.main import run_cli
from web_app import app

logger = logging.getLogger()

def setup():
    load_dotenv()

    bugsnag.configure(
        api_key=os.getenv('BUGSNAG_API_KEY'),
    )

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log")
    ])
    handler = BugsnagHandler()
    # Send only ERROR-level logs and above
    handler.setLevel(logging.WARNING)
    logger.addHandler(handler)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        run_cli()
    else:
        app.run(debug=True)