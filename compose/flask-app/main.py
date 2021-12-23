import logging
import argparse
import sys
import os
from logging import DEBUG, INFO
from os import path
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from flask import Flask, current_app, request

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
    default_db_host = os.getenv("DB_HOST", "localhost")
    default_db_user = os.getenv("DB_USER", "root")
    default_db_pass = os.getenv("DB_PASS", "root")
    default_db_name = os.getenv("DB_NAME", "flights")

    parser = argparse.ArgumentParser(description="Airports Docker Parser")
    # parser.add_argument('action', choices=('print', 'version', 'history'), help='what to do?')
    parser.add_argument('-s', '--host', default=default_db_host, help='database host')
    parser.add_argument('-u', '--user', default=default_db_user, help='database user')
    parser.add_argument('-p', '--pswd', default=default_db_pass, help='database password')
    parser.add_argument('-d', '--database', default=default_db_name, help='database name')
    args, _ = parser.parse_known_args()
    return args


# get command line args
args = set_args()
logger.info(f"flask mysql config: host={args.host} user={args.user} db={args.database}")
logger.info(f"starting flask app")
# create flask app and sqlalchemy engine
app = Flask(__name__)
engine = create_engine(f"mysql+pymysql://{args.user}:{args.pswd}@{args.host}/{args.database}?charset=utf8mb4", 
                       poolclass=QueuePool, pool_size=5, max_overflow=0)
app.config['engine'] = engine


@app.route('/')
def airport():
    """main GET route to search and return a aiport by iata code"""
    iata = request.args.get('iata', default=None)
    engine = current_app.config['engine']
    logger.info(f"query db for iata: {str(iata)}")
    with engine.connect() as conn:
        if iata is not None:
            # search for specific iata airport code
            result = conn.execute(
                text("select iata, name, city, state, lat, lng, tz from airports where iata = :iata"),
                {'iata': str(iata).strip().upper()}
            )
            result = result.mappings()
            row = result.first()
            if row is not None:
                # return a single airport result
                return {
                    'iata' : iata,
                    'results': [{k: v for k, v in row.items()}]
                } 
            else:
                # airport code not found, return empty list
                return {
                    'iata' : iata,
                    'results': []
                } 
        else:
            # no iata code provided, return all airports
            logger.info(f"returning all airports")
            result = conn.execute(
                text("select iata, name, city, state, lat, lng, tz from airports order by iata")
            )
            rows = result.mappings().all()
            return {
                'iata' : iata,
                'results': [{k: v for k, v in row.items()} for row in rows]
            }


if __name__ == "__main__":
    # run flask app on port 5000
    app.run('0.0.0.0', 5000)
