from flask import Flask
from backend.server import app

import logging

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('hello world')

if __name__ == "__main__":
    main()
