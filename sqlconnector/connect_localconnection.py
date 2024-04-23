import os

import sqlalchemy
# import mysql
import pymysql
from dotenv import load_dotenv

load_dotenv()

user=os.getenv('DB_USERNAME')
password=os.getenv('DB_PASSWORD')
database=os.getenv('DB_NAME')
hostconn=os.getenv('LOCAL_CONNECTION_IP')


def local_conn():
    connection = sqlalchemy.create_engine(f"mysql+pymysql://{user}:{password}@{hostconn}/{database}")
    # pyconnection = pymysql.connect(host="localhost",
    #                             user=os.getenv('DB_USERNAME'),
    #                             password=os.getenv('DB_PASSWORD'),
    #                             database=os.getenv('DB_NAME'),
    #                             )

    with connection.connect() as connect:
        result =  connect.execute(sqlalchemy.text("SELECT * FROM characters"))
        print(result.fetchone())

    return connection

    # try:
    #     with pyconnection:
    #         with pyconnection.cursor() as cursor:
    #             cursor.execute("SELECT * from characters")
    #             result = cursor.fetchall()
    #             print(result)
    # except Exception as e:
    #     print(e)


# [END cloud_sql_mysql_sqlalchemy_connect_connector]