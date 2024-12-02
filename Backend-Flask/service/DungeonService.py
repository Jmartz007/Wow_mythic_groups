import logging

import sqlalchemy
from sqlalchemy import exc

from datagatherer.dungeondata import get_all_dugeons_db, delete_dungeon
from utils.customexceptions import DatabaseError

logger = logging.getLogger(f"main.{__name__}")


def get_dungeons_all() -> dict:
    try:
        results = get_all_dugeons_db()
        dungeons_list = [{"id": id, "dungeon": dungeon} for id, dungeon in results]
        logger.debug(f"formatted return value: {dungeons_list}")
        return dungeons_list
    except exc.SQLAlchemyError as e:
        logger.error(e)
        raise DatabaseError
