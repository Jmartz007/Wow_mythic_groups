import logging

import sqlalchemy
from sqlalchemy import exc, Table, MetaData

from utils.customexceptions import DatabaseError

if __name__ == "__main__":
    from sqlconnector.connect_localconnection import local_conn

    db = local_conn()

else:
    from sqlconnector.connection_pool import init_connection_pool

    db = init_connection_pool()

logger = logging.getLogger(f"main.{__name__}")


def get_all_dugeons_db():
    with db.connect() as conn:
        results = conn.execute(sqlalchemy.text("""SELECT * FROM Dungeon""")).fetchall()
    # logger.debug(f"database results: {results}")
    return results


def db_get_dungeon_by_id(id: int):
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(""" SELECT * FROM Dungeon WHERE idDungeon = :id """).params(
                {"id": id}
            )
        ).one_or_none()
    return result


def db_get_dungeon_by_name(id: str):
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                """ SELECT * FROM Dungeon WHERE DungeonName = :id """
            ).params({"id": id})
        ).one_or_none()
    return result


def post_new_dungeon_db(dungeon: str):
    with db.connect() as conn:
        # Using the SQL Alchemy ORM just to be able to get the inserted primary key of the new object.
        metadata = MetaData()
        metadata.reflect(bind=conn)
        dungeon_table = Table("Dungeon", metadata, autoload_with=conn)
        exist = conn.execute(
            sqlalchemy.text(
                """SELECT * FROM Dungeon
            WHERE DungeonName = :dungeon"""
            ),
            {"dungeon": dungeon},
        ).one_or_none()
        if not exist:
            logger.info(f"Adding dungeon {dungeon}")
            result = conn.execute(
                dungeon_table.insert().values(DungeonName=dungeon)
            ).inserted_primary_key

            conn.commit()
            logger.info(f"{dungeon} added successfully")
            return result
        else:
            logger.info(f"{dungeon} already in list")
            raise DatabaseError("Dungeon already in list")


def db_del_dungeon_by_id(id: int) -> int:
    logger.info(f"Dungeon ID to delete {id}")
    try:
        with db.connect() as conn:
            result = conn.execute(
                sqlalchemy.text(""" DELETE FROM Dungeon WHERE idDungeon = :id """),
                {"id": id},
            ).rowcount
            conn.commit()
        logger.info(f"Deleted {result} dungeon {id}")
        return result
    except exc.IntegrityError as e:
        logger.debug(e)
        logger.warning(
            f"Cannot delete dungeon with ID {id}, still in use by characters"
        )
        raise DatabaseError(
            f"Cannot delete dungeon with ID {id}, still in use by characters"
        )
    except exc.SQLAlchemyError as e:
        logger.exception(e)
        raise DatabaseError from e


def db_del_dungeon_by_name(dungeon: str) -> int:
    logger.info(f"Dungeon name to delete {dungeon}")
    try:
        with db.connect() as conn:

            result = conn.execute(
                sqlalchemy.text(
                    """DELETE FROM Dungeon
                WHERE DungeonName = :dungeon"""
                ),
                {"dungeon": dungeon},
            ).rowcount
            conn.commit()
        logger.info(f"Deleted {result} dungeon {dungeon}")
        return result
    except exc.IntegrityError as e:
        logger.debug(e)
        logger.warning(f"Cannot delete dungeon {dungeon}, still in use by characters")
        raise DatabaseError(
            f"Cannot delete dungeon {dungeon}, still in use by characters"
        )
    except exc.SQLAlchemyError as e:
        logger.exception(e)
        raise DatabaseError from e
