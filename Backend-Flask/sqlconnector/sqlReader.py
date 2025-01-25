import logging

import sqlalchemy
from sqlalchemy import exc
from flask import Response


if __name__ == "__main__":
    from .connect_localconnection import local_conn

    db = local_conn()
else:
    from .connection_pool import init_connection_pool

    db = init_connection_pool()

logger = logging.getLogger(f"main.{__name__}")


def create_player_dict(player_entries, char_entries, role_entries):
    try:
        player_dict = {}
        # add results to dictionary and create a value of type dict as the entry for that key
        for row in player_entries:
            player_dict[row[1]] = {}

    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
    except Exception as error:
        logger.exception(error)

    # add characters to the player entries
    try:
        for row in char_entries:
            for key, value in player_dict.items():
                if key == row[0] and (len(value) == 0):
                    player_dict[row[0]] = {
                        row[1]: {
                            "Class": row[2],
                            "Range": row[3],
                            "Skill Level": row[4],
                            "Dungeon": row[5],
                            "Key Level": row[6],
                            "is_active": row[7],
                        }
                    }  # <--- where to add a characters information to the
                elif key == row[0]:
                    player_dict[row[0]].update(
                        {
                            row[1]: {
                                "Class": row[2],
                                "Range": row[3],
                                "Skill Level": row[4],
                                "Dungeon": row[5],
                                "Key Level": row[6],
                                "is_active": row[7],
                            }
                        }
                    )  # <----------- here too
                else:
                    # print("row did not match key\n")
                    continue
        logger.info("Characters added to players dictionary")
    except Exception as error:
        logger.exception(error)

    # add role information to the characters in the dictionary
    try:
        newDict = {}
        for i in role_entries:
            # logger.debug(i)
            # creating a new list to add multiple roles if needed
            newList = []
            if i[0] in newDict.keys():
                if len(newDict[i[0]]["Role"]) >= 2:
                    newList.extend(
                        [newDict[i[0]]["Role"][0], newDict[i[0]]["Role"][1], i[1]]
                    )
                    if i[1] == "Tank":
                        newDict[i[0]].update({"Role": newList, "Tank Skill": i[3]})
                    elif i[1] == "Healer":
                        newDict[i[0]].update({"Role": newList, "Healer Skill": i[3]})
                    elif i[1] == "DPS":
                        newDict[i[0]].update({"Role": newList, "DPS Skill": i[3]})
                    continue

                newList.extend([newDict[i[0]]["Role"][0], i[1]])

                if i[1] == "Tank":
                    newDict[i[0]].update({"Role": newList, "Tank Skill": i[3]})
                elif i[1] == "Healer":
                    newDict[i[0]].update({"Role": newList, "Healer Skill": i[3]})
                elif i[1] == "DPS":
                    newDict[i[0]].update({"Role": newList, "DPS Skill": i[3]})

            else:
                newList.append(i[1])
                if i[1] == "Tank":
                    newDict.update({i[0]: {"Role": newList, "Tank Skill": i[3]}})
                elif i[1] == "Healer":
                    newDict.update({i[0]: {"Role": newList, "Healer Skill": i[3]}})
                elif i[1] == "DPS":
                    newDict.update({i[0]: {"Role": newList, "DPS Skill": i[3]}})

        # print(newDict)
        for key, value in newDict.items():
            for k, v in player_dict.items():
                if key in v:
                    player_dict[k][key].update(value)
        logger.debug(player_dict)
        logger.info("sqlReader successfully created dictionary from database")

    except Exception as error:
        logger.error(error)

    return player_dict


def get_key_info(CharacterName: str):
    with db.connect() as conn:
        MythicKey = conn.execute(
            sqlalchemy.text(
                """SELECT CharacterName, DungeonName, level FROM char_info
            WHERE CharacterName = :characterName"""
            ),
            {"characterName": CharacterName},
        ).first()
        return MythicKey


def edit_key_info(CharacterName: str, level: str, dungeon: str):
    with db.connect() as conn:
        MythicKey_ID = conn.execute(
            sqlalchemy.text(
                """SELECT MythicKey_id FROM `character`
            WHERE CharacterName = :characterName"""
            ),
            {"characterName": CharacterName},
        ).one_or_none()

        results = conn.execute(
            sqlalchemy.text(
                """UPDATE mythickey
            SET level = :level,
            Dungeon_id = (SELECT idDungeon FROM dungeon WHERE DungeonName = :dungeonName)
            WHERE idMythicKey = :mythickey_id"""
            ),
            {"level": level, "dungeonName": dungeon, "mythickey_id": MythicKey_ID[0]},
        ).rowcount
        logger.info(f"Updating key for {CharacterName} to {level}-{dungeon}")
        conn.commit()
    return results


def get_dugeons_list():
    with db.connect() as conn:
        results = conn.execute(sqlalchemy.text("""SELECT * from dungeon""")).fetchall()

    logger.debug(f"databse results: {results}")
    dungeons_list = {k: v for k, v in results}
    logger.debug(f"formatted return value: {dungeons_list}")
    return dungeons_list


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


def delete_dungeon(dungeon):
    logger.info(f"Dungeon to delete {dungeon}")
    with db.connect() as conn:
        try:
            result = conn.execute(
                sqlalchemy.text(
                    """DELETE FROM dungeon
                WHERE DungeonName = :dungeon"""
                ),
                {"dungeon": dungeon},
            ).rowcount
            conn.commit()
        except exc.IntegrityError as e:
            logger.debug(e)
            logger.info(f"Cannot delete {dungeon}, still in use by characters")
            return f"Cannot delete {dungeon}, still in use by characters"
        else:
            logger.info(f"Deleted {result} dungeon {dungeon}")
            return result


def clear_database():
    try:
        with db.connect() as conn:
            conn.execute(sqlalchemy.text("DELETE FROM role_entries"))
            conn.execute(sqlalchemy.text("DELETE FROM characters"))
            conn.execute(sqlalchemy.text("DELETE FROM players"))

            conn.commit()
            logger.info("Database Cleared")
    except Exception as error:
        print("Error occurred - ", error)
        logger.exception(error)


def check_session_exists(groupid):
    try:
        with db.connect() as conn:
            query = conn.execute(
                sqlalchemy.text(
                    f"SELECT group_ID FROM `player` WHERE group_ID = {groupid}"
                )
            ).fetchall()
            numFound = len(query)
            logger.debug(f"len of results: {numFound}")

            if numFound >= 1:
                logger.info("results found")
                return True
            else:
                logger.info("No results found")
                return False
    except Exception as error:
        logger.exception(error)
