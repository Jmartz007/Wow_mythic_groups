import logging

import sqlalchemy
from sqlalchemy import exc

if __name__ == "__main__":
    from sqlconnector.connect_localconnection import local_conn

    db = local_conn()

else:
    from sqlconnector.connection_pool import init_connection_pool

    db = init_connection_pool()

logger = logging.getLogger(f"main.{__name__}")


def db_get_key_info_by_id(key_id: int):
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                """SELECT m.idMythicKey, m.level, m.Dungeon_id, d.DungeonName
            FROM mythickey m
            LEFT JOIN dungeon d ON m.Dungeon_id = d.idDungeon
            WHERE m.idMythicKey = :keyid"""
            ),
            {"keyid": key_id},
        ).one_or_none()

    return result
