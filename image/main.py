"""
DSA - Ch5Ep2
Introduction to Docker & Dockerfile

Simple script to read a file and print to the console.
This script demonstrates how to add files and run a command using docker.


"""
import logging
from logging import DEBUG, INFO
import sys
from os import path


# setup logging and logger
logging.basicConfig(format='[%(levelname)-5s][%(asctime)s][%(module)s:%(lineno)04d] : %(message)s',
                    level=INFO,
                    stream=sys.stdout)
logger: logging.Logger = logging


def run(filename='./names.txt'):
    """
    Read a file called names.txt and print the content to the console
    """
    if path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                logger.info(line.strip())
    else:
        logger.error(f"Could not find the input file: {filename}")


if __name__ == "__main__":
    run()
