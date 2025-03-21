import os
import logging


import sqlalchemy
import pymysql
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(f"main.{__name__}")

user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
hostconn = os.getenv("LOCAL_CONNECTION_IP")


def local_conn():
    try:
        connection = sqlalchemy.create_engine(
            f"mysql+pymysql://{user}:{password}@{hostconn}/{database}",
            pool_size=10,
            pool_recycle=1800,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 8}
        )

        with connection.connect() as connect:
            result = connect.execute(sqlalchemy.text("SHOW TABLES")).fetchall()
            logger.info(result)
            return connection
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    local_conn()
