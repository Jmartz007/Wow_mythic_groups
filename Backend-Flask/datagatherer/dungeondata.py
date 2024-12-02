import logging

import sqlalchemy
from sqlalchemy import exc

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
        results = conn.execute(sqlalchemy.text("""SELECT * from dungeon""")).fetchall()

    logger.debug(f"databse results: {results}")

    return results


def post_new_dungeon(dungeon):
    with db.connect() as conn:
        exist = conn.execute(
            sqlalchemy.text(
                """SELECT * FROM dungeon
            WHERE DungeonName = :dungeon"""
            ),
            {"dungeon": dungeon},
        ).one_or_none()
        if not exist:
            try:
                logger.info(f"Adding dungeon {dungeon}")
                conn.execute(
                    sqlalchemy.text(
                        """INSERT INTO dungeon (DungeonName)
                    VALUES (:dungeon)"""
                    ),
                    {"dungeon": dungeon},
                )
                conn.commit()
            except exc.StatementError as err:
                logger.exception(err)
                return "An error occurred in the database"
            else:
                logger.info(f"{dungeon} added successfully")
                return f"{dungeon} added successfully"
        else:
            logger.info(f"{dungeon} already in list")
            return f"{dungeon} already in list"


def delete_dungeon(dungeon: str) -> int:
    logger.info(f"Dungeon to delete {dungeon}")
    try:
        with db.connect() as conn:

            result = conn.execute(
                sqlalchemy.text(
                    """DELETE FROM dungeon
                WHERE DungeonName = :dungeon"""
                ),
                {"dungeon": dungeon},
            ).rowcount
            conn.commit()
        logger.info(f"Deleted {result} dungeon {dungeon}")
        return result
    except exc.IntegrityError as e:
        logger.debug(e)
        logger.warning(f"Cannot delete {dungeon}, still in use by characters")
        raise DatabaseError(f"Cannot delete {dungeon}, still in use by characters")
    except exc.SQLAlchemyError as e:
        logger.exception(e)
        raise DatabaseError from e
