import logging

from pymysql import IntegrityError
import sqlalchemy
from sqlalchemy import exc

from datagatherer.dungeondata import (
    db_del_dungeon_by_id,
    db_del_dungeon_by_name,
    db_get_dungeon_by_id,
    db_get_dungeon_by_name,
    get_all_dugeons_db,
    post_new_dungeon_db,
)
from utils.customexceptions import DatabaseError, DataNotFoundError, ServiceException

logger = logging.getLogger(f"main.{__name__}")


def get_dungeons_all() -> list[dict]:
    try:
        results = get_all_dugeons_db()
        dungeons_list = [{"id": id, "dungeon": dungeon} for id, dungeon in results]
        # logger.debug(f"formatted return value: {dungeons_list}")
        return dungeons_list
    except exc.SQLAlchemyError as e:
        logger.error(e)
        raise DatabaseError


def get_dungeon_by_id_or_name(id: int):
    try:
        id = int(id)
    except:
        logger.debug("id is not a number")
    try:
        logger.debug(f"id is a {type(id)}")
        if type(id) == int:
            result = db_get_dungeon_by_id(id)
        elif type(id) == str:
            result = db_get_dungeon_by_name(id)
        else:
            logger.warning("dungeon id must be int or str")
            raise TypeError("dungeon id must be int or str")

        if not result:
            logger.warning(f"No data found for {id}")
            raise DataNotFoundError(input=id)
        dungeon_id, dungeon_name = result
        dungeon_result = {"id": dungeon_id, "dungeon": dungeon_name}
        return dungeon_result
    except exc.SQLAlchemyError as e:
        logger.error(e)
        raise DatabaseError


def del_dungeon_by_id_or_name(dungeon_id: int | str):
    """Deletes a dungeon by id number or string name"""
    try:
        dungeon_id = int(dungeon_id)
    except ValueError:
        logger.debug("id is not a number")
    if dungeon_id.lower() == "unknown" or dungeon_id == 1:
        raise ServiceException("the dungeon 'Unknown' is not deletable")
    try:
        logger.debug("id is a %s", type(dungeon_id))
        if isinstance(dungeon_id, int):
            result = db_del_dungeon_by_id(dungeon_id)
        elif type(dungeon_id) == str:
            result = db_del_dungeon_by_name(dungeon_id)
        else:
            logger.warning("dungeon id must be int or str")
            raise TypeError("dungeon id must be int or str")

        if result < 1:
            logger.warning("result is less than 0")
            raise DataNotFoundError(input=dungeon_id)
        logger.debug("result is %s", result)
        return result
    except DatabaseError as e:
        logger.error(e)
        raise DatabaseError(e) from e


def add_dungeon(dungeon_name: str):
    try:
        result = post_new_dungeon_db(dungeon_name)
        new_dungeon = {"id": result[0], "dungeon": dungeon_name}
        logger.debug(new_dungeon)
        return new_dungeon
    except exc.IntegrityError as e:
        logger.exception(e)
        raise ValueError from e
    except DatabaseError as e:
        logger.error(e)
        raise e
    except exc.SQLAlchemyError as e:
        logger.exception(e)
        raise DatabaseError from e
    except Exception as e:
        logger.exception(e)
        raise Exception from e
