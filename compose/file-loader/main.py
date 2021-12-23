"""
DSA - Ch4Ep2
Advanced Dockerfile

Demonstrate saving state with docker volume.
This script saves history of each run using a sqlite3 databases.
Docker image uses a VOLUME to save the sqlite database in between runs.
"""

import logging
import argparse
import sys
import os
from logging import DEBUG, INFO
from os import path
import pandas as pd
from sqlalchemy import create_engine


# setup logging and logger
logging.basicConfig(format='[%(levelname)-5s][%(asctime)s][%(module)s:%(lineno)04d] : %(message)s',
                    level=INFO,
                    stream=sys.stderr)
logger: logging.Logger = logging


def set_args():
    """
    Define cmdline args
    """
    # add reading environment variables as default args
    default_inputfile = os.getenv("INPUT_FILE", "./deb-airports.csv")
    default_db_host = os.getenv("DB_HOST", "localhost")
    default_db_user = os.getenv("DB_USER", "root")
    default_db_pass = os.getenv("DB_PASS", "root")
    default_db_name = os.getenv("DB_NAME", "flights")

    parser = argparse.ArgumentParser(description="Airports Docker Parser")
    # parser.add_argument('action', choices=('print', 'version', 'history'), help='what to do?')
    parser.add_argument('-i', '--input', default=default_inputfile, help='source input file')
    parser.add_argument('-s', '--host', default=default_db_host, help='database host')
    parser.add_argument('-u', '--user', default=default_db_user, help='database user')
    parser.add_argument('-p', '--pswd', default=default_db_pass, help='database password')
    parser.add_argument('-d', '--database', default=default_db_name, help='database name')
    args, _ = parser.parse_known_args()
    return args


def run():
    """
    Read airports csv & load into MySQL using SQLAlchemy and pnadas
    """
    # read cmdline args
    args = set_args()

    # create mysql engine
    logger.info(f"connecting to mysql: host={args.host} user={args.user} db={args.database}")
    engine = create_engine(f"mysql+pymysql://{args.user}:{args.pswd}@{args.host}/{args.database}?charset=utf8mb4")
    
    # read airports csv file and check columns
    filepath = args.input
    logger.info(f"reading airports file: '{filepath}'")
    df = pd.read_csv(filepath, header=0, index_col='iata')
    # check all columns exist
    if not all([col in list(df.columns) for col in ('name', 'city', 'state', 'lat', 'lng', 'tz')]):
        raise ValueError(f"mismatching airports file schema. not all columns are present!")
    logger.info(f"read {len(df.index)} rows from the file")

    # insert rows into mysql using pandas
    logger.info(f"inserting rows into database")
    df.to_sql('airports', engine, if_exists='replace', chunksize=2000)
    logger.info("done")


if __name__ == "__main__":
    run()
