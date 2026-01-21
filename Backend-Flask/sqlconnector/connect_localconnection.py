"""Establishes a local connection to the database using SQLAlchemy."""

import logging

import sqlalchemy
from sqlalchemy.engine import URL
import sqlalchemy.exc
from dotenv import load_dotenv

from sqlconnector.db_config import DBConfig

load_dotenv()

logger = logging.getLogger(f"main.{__name__}")


def local_conn(config: DBConfig) -> sqlalchemy.engine.base.Engine:
    "use a local TCP connection when LOCAL_CONNECTION_IP is defined"
    try:
        url = URL.create(
            "mysql+pymysql",
            username=config.user,
            password=config.password,
            host=config.instance_host,
            database=config.database,
        )
        engine = sqlalchemy.create_engine(
            url,
            pool_size=10,
            pool_recycle=1800,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 8},
        )

        return engine

    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error(f"SQLAlchemy Error: {e}")
        raise
    except Exception as e:
        logger.error(e)
        raise


if __name__ == "__main__":
    local_conn(DBConfig.from_env())  # for testing purposes only
