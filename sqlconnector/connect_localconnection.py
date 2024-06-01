import os

import sqlalchemy
import pymysql
from dotenv import load_dotenv

load_dotenv()

user=os.getenv('DB_USERNAME')
password=os.getenv('DB_PASSWORD')
database=os.getenv('DB_NAME')
hostconn=os.getenv('LOCAL_CONNECTION_IP')


def local_conn():
    connection = sqlalchemy.create_engine(f"mysql+pymysql://{user}:{password}@{hostconn}/{database}")

    with connection.connect() as connect:
        result =  connect.execute(sqlalchemy.text("SELECT * FROM `character`"))

    return connection