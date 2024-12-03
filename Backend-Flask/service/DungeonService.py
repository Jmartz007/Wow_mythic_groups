import logging

from pymysql import IntegrityError
import sqlalchemy
from sqlalchemy import exc

from datagatherer.dungeondata import (
    db_del_dungeon_by_id,
    db_del_dungeon_by_name,
    db_get_dungeon,
    get_all_dugeons_db,
    post_new_dungeon_db,
)
from utils.customexceptions import DatabaseError, DataNotFoundError

logger = logging.getLogger(f"main.{__name__}")


def get_dungeons_all() -> list[dict]:
    try:
        results = get_all_dugeons_db()
        dungeons_list = [{"id": id, "dungeon": dungeon} for id, dungeon in results]
        logger.debug(f"formatted return value: {dungeons_list}")
        return dungeons_list
    except exc.SQLAlchemyError as e:
        logger.error(e)
        raise DatabaseError


def get_dungeon_by_id(id: int):
    try:
        result = db_get_dungeon(id)
        if not result:
            raise DataNotFoundError(input=id)
        dungeon_id, dungeon_name = result
        dungeon_result = {"id": dungeon_id, "dungeon": dungeon_name}
        return dungeon_result
    except exc.SQLAlchemyError:
        raise DatabaseError


def del_dungeon_by_id_or_name(id: int | str):
    try:
        id = int(id)
    except:
        logger.debug("id is not a number")
    try:
        logger.debug(f"id is a {type(id)}")
        if type(id) == int:
            result = db_del_dungeon_by_id(id)
        elif type(id) == str:
            result = db_del_dungeon_by_name(id)
        else:
            raise TypeError("dungeon id must be int or str")

        if result < 1:
            logger.debug("result is less than 0")
            raise DataNotFoundError(input=id)
        logger.debug(f"result is {result}")
        return result
    except DatabaseError as e:
        logger.error(e)
        raise DatabaseError(e)


def add_dungeon(dungeon_name: str):
    try:
        result = post_new_dungeon_db(dungeon_name)
        new_dungeon = {"id": result[0], "dungeon": dungeon_name}
        logger.debug(new_dungeon)
        return new_dungeon
    except exc.IntegrityError as e:
        logger.exception(e)
        raise ValueError from e
    except exc.SQLAlchemyError as e:
        logger.exception(e)
        raise DatabaseError from e
    except Exception as e:
        logger.exception(e)
        raise Exception from e
