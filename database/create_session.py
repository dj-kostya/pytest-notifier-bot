import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from database.models import Base
from data.config import PGUSER, PGPASSWORD, PGHOST, PGPORT, PGDB


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DB_CONFIG = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDB}'
engine = create_engine(DB_CONFIG)
try:
    recreate_database()
except OperationalError:
    logging.error('Could not connect to database!')
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()
