"""This Module has database functions with SQL queries for getting Mythic Key related information"""

import logging

import sqlalchemy
from sqlalchemy import exc

from datagatherer.playerdata import db_find_character_by_name
from datagatherer.dungeondata import db_get_dungeon_by_name
from utils.customexceptions import DatabaseError

if __name__ == "__main__":
    from sqlconnector.connect_localconnection import local_conn

    db = local_conn()

else:
    from sqlconnector.connection_pool import init_connection_pool

    db = init_connection_pool()

logger = logging.getLogger(f"main.{__name__}")


def db_get_key_info_by_id(key_id: int):
    """Database query to find the mythic key entry information based on the mythic key id"""
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                """SELECT m.idMythicKey, m.level, m.Dungeon_id, d.DungeonName
            FROM MythicKey m
            LEFT JOIN Dungeon d ON m.Dungeon_id = d.idDungeon
            WHERE m.idMythicKey = :keyid"""
            ),
            {"keyid": key_id},
        ).one_or_none()

    return result


def db_udpate_key_data(
    character_name: str, new_dungeon: str = None, new_level: int = None
):
    """Database query that updates the mythic key info for the character"""
    with db.connect() as conn:
        try:
            key_id = db_find_character_by_name(character_name)[4]
            logger.debug("Key id: %s", key_id)

            update_fields = {}
            if new_dungeon is not None:
                new_dungeon_id = db_get_dungeon_by_name(new_dungeon)[0]
                update_fields["Dungeon_id"] = new_dungeon_id
            if new_level is not None:
                update_fields["level"] = new_level

            set_clause = ", ".join([f"{key} = :{key}" for key in update_fields.keys()])
            update_query = (
                f"UPDATE MythicKey SET {set_clause} WHERE idMythicKey = :key_id"
            )
            update_fields["key_id"] = key_id
            update = conn.execute(sqlalchemy.text(update_query), update_fields)
            conn.commit()
            logger.debug("Updated rows: %s", update.rowcount)
            return update.rowcount
        except exc.SQLAlchemyError as e:
            logger.error("A sql error occurred: %s", e)
            raise DatabaseError("An error occurred in the database")
