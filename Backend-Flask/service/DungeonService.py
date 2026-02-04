import logging

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


def get_dungeon_by_id_or_name(id: str | int):
    try:
        id = int(id)
    except ValueError:
        logger.debug("id is not a number")
    try:
        logger.debug(f"id is a {type(id)}")
        if type(id) is int:
            result = db_get_dungeon_by_id(id)
        elif type(id) is str:
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


def _validate_id(dungeon_id: str | int):
    try:
        int_id = int(dungeon_id)
        if int_id == 1:
            raise ServiceException("the dungeon 'Unknown' is not deletable")
        return int_id
    except ValueError:
        pass
    if type(dungeon_id) is str and dungeon_id.lower() == "unknown":
        raise ServiceException("the dungeon 'Unknown' is not deletable")
    else:
        return dungeon_id


def del_dungeon_by_id_or_name(dungeon_id: int | str):
    """Deletes a dungeon by id number or string name"""
    dungeon_id = _validate_id(dungeon_id)
    try:
        logger.debug("id is a %s", type(dungeon_id))
        if type(dungeon_id) is int:
            result = db_del_dungeon_by_id(dungeon_id)
        elif type(dungeon_id) is str:
            result = db_del_dungeon_by_name(dungeon_id)
        else:
            logger.warning("dungeon id must be int or str")
            raise TypeError("dungeon id must be int or str")

        if result < 1:
            logger.warning("result is less than 0")
            raise DataNotFoundError(input=dungeon_id)
        logger.debug("result is %s", result)
        return result
    except Exception as e:
        logger.exception(e)
        raise ServiceException("Failed to delete dungeon")


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
        raise
    except exc.SQLAlchemyError as e:
        logger.exception(e)
        raise DatabaseError from e
    except Exception as e:
        logger.exception(e)
        raise ServiceException("General failure adding dungeon") from e
