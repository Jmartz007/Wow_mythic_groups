import logging
from ast import Dict, List, Try
from re import DEBUG

import sqlalchemy
from sqlalchemy import exc
from flask import Response


if __name__ == "__main__":
    from connect_localconnection import local_conn

    db = local_conn()
else:
    from .connection_pool import init_connection_pool

    db = init_connection_pool()

logger = logging.getLogger(f"main.{__name__}")


def create_dict_from_db(is_active: bool = False) -> dict:
    """Retrieves players from the DB and adds them to a dictionary"""
    player_dict = {}
    try:
        with db.connect() as conn:
            # Execute the query and fetch all results

            if is_active:
                player_entries = conn.execute(
                    sqlalchemy.text(
                        f"""SELECT p.idPlayers, p.PlayerName
                        FROM player p
                        JOIN `character` `c` on p.idPlayers = `c`.Player_idPlayers
                        WHERE  `c`.is_active = 1"""
                    )
                ).fetchall()
                charEntries = conn.execute(
                    sqlalchemy.text(
                        f"""SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                        FROM char_info
                        WHERE is_active = 1"""
                    )
                ).fetchall()
            else:
                player_entries = conn.execute(
                    sqlalchemy.text(f"SELECT * FROM player")
                ).fetchall()
                charEntries = conn.execute(
                    sqlalchemy.text(
                        f"""SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                        FROM char_info"""
                    )
                ).fetchall()
            logger.debug(charEntries)
            logger.info("Query from tables (players, characters) executed successfully")

            roleEntries = conn.execute(
                sqlalchemy.text(
                    f"""SELECT c.CharacterName, pr.PartyRoleName, c.ClassName, cr.RoleSkill FROM `character` as c
                JOIN combatrole_has_character AS cr ON cr.Character_idCharacter = c.idCharacter
                JOIN partyrole AS pr ON pr.idPartyRole = cr.PartyRole_idPartyRole
                """
                )
            ).fetchall()
            logger.info(
                "Query from tables (character, combatrole_has_character, partyrole) executed successfully"
            )

        # add results to dictionary and create a value of type dict as the entry for that key
        for row in player_entries:
            player_dict[row[1]] = {}

    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
        raise ValueError("Could not find player entries")

    # add characters to the player entries
    try:
        for row in charEntries:
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
        for i in roleEntries:
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


def read_active_players(is_active: dict):
    try:
        with db.connect() as conn:

            activate = list(is_active.keys())

            placeholders = ", ".join(f":activate_{i}" for i in range(len(activate)))

            set_active = sqlalchemy.text(
                f"""
            UPDATE `character`
            SET `is_active` = 1
            WHERE CharacterName IN ({placeholders})
            """
            )
            set_inactive = sqlalchemy.text(
                f"""
            UPDATE `character`
            SET `is_active` = 0
            WHERE CharacterName NOT IN ({placeholders})
            """
            )

            parameters = {f"activate_{i}": name for i, name in enumerate(activate)}

            conn.execute(set_active, parameters)
            conn.execute(set_inactive, parameters)

            conn.commit()
            """
                SELECT DISTINCT
                    `p`.`PlayerName` AS `PlayerName`,
                    `c`.`CharacterName` AS `CharacterName`,
                    `c`.`ClassName` AS `ClassName`,
                    `c`.`is_active` AS `is_active`
                FROM
                    (`player` `p`
                    JOIN `character` `c` ON ((`c`.`Player_idPlayers` = `p`.`idPlayers`)))
                WHERE
                    `c`.`is_active` = 1
                ORDER BY `p`.`PlayerName`
            """
            # Execute the query and fetch all results
            player_entries = conn.execute(
                sqlalchemy.text(
                    f"""SELECT p.idPlayers, p.PlayerName
                                FROM player p
                                JOIN `character` `c` on p.idPlayers = `c`.Player_idPlayers
                                WHERE  `c`.is_active = 1"""
                )
            ).fetchall()

            charEntries = conn.execute(
                sqlalchemy.text(
                    f"""SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                    FROM char_info
                    WHERE is_active = 1
                    """
                )
            ).fetchall()
            logger.debug(charEntries)
            logger.info("Query from tables (players, characters) executed successfully")

            roleEntries = conn.execute(
                sqlalchemy.text(
                    f"""SELECT c.CharacterName, pr.PartyRoleName, c.ClassName, cr.RoleSkill FROM `character` as c
                JOIN combatrole_has_character AS cr ON cr.Character_idCharacter = c.idCharacter
                JOIN partyrole AS pr ON pr.idPartyRole = cr.PartyRole_idPartyRole
                """
                )
            ).fetchall()
            logger.info(
                "Query from tables (character, combatrole_has_character, partyrole) executed successfully"
            )

            return player_entries, charEntries, roleEntries

    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
    except Exception as error:
        logger.exception(error)


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


def delete_player(PlayerName: str):
    try:
        with db.connect() as conn:
            conn.execute(
                sqlalchemy.text(
                    """
                DELETE FROM `combatrole_has_character`
                WHERE `Character_idCharacter` IN (
                    SELECT idCharacter FROM `character`
                    JOIN player ON idPlayers = Player_idPlayers
                    WHERE `player`.`PlayerName` = :playerName);
                """
                ),
                {"playerName": PlayerName},
            )
            char_result = conn.execute(
                sqlalchemy.text(
                    """
                DELETE FROM `character` 
                WHERE Player_idPlayers IN (
                    SELECT idPlayers FROM `player`
                    WHERE `player`.`PlayerName` = :playerName);
                """
                ),
                {"playerName": PlayerName},
            )
            player_result = conn.execute(
                sqlalchemy.text(
                    """
                DELETE FROM `player`
                WHERE `player`.`PlayerName` = :playerName;
                """
                ),
                {"playerName": PlayerName},
            )
            conn.commit()
        logger.info(
            f"Deleted {PlayerName} and {char_result.rowcount} characters associated"
        )
        return f"Deleted {PlayerName} and {char_result.rowcount} characters associated"

    except exc.StatementError as sqlstatementerr:
        logger.exception(sqlstatementerr)
    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
        return Response(status=400, response=f"SQL Error: {sqlerror}")
    except Exception as e:
        logger.exception(e)
        return Response(status=500, response="Error deleting player")


def delete_character(CharacterName: str):
    try:
        with db.connect() as conn:

            Player_ID = conn.execute(
                sqlalchemy.text(
                    """SELECT idPlayers FROM player
                JOIN `character` c ON c.Player_idPlayers = idPlayers
                WHERE CharacterName = :characterName"""
                ),
                {"characterName": CharacterName},
            ).one()

            Player_ID = Player_ID[0]

            conn.execute(
                sqlalchemy.text(
                    """DELETE FROM `combatrole_has_character`
                WHERE `Character_idCharacter` IN (
                SELECT idCharacter FROM `character`
                WHERE `character`.`CharacterName` = :characterName)"""
                ),
                {"characterName": CharacterName},
            )
            result = conn.execute(
                sqlalchemy.text(
                    """DELETE FROM `character`
                WHERE `CharacterName` = :characterName"""
                ),
                {"characterName": CharacterName},
            )

            conn.commit()

            last_player = conn.execute(
                sqlalchemy.text(
                    f"""SELECT Player_idPlayers FROM `character`
                JOIN player ON idPlayers = Player_idPlayers
                WHERE Player_idPlayers = {Player_ID} 
                """
                )
            ).all()
            print(last_player)
            print(len(last_player))
            if len(last_player) == 0:
                player_del = conn.execute(
                    sqlalchemy.text(
                        """
                DELETE FROM `player`
                WHERE `player`.`idPlayers` = :playerID;
                """
                    ),
                    {"playerID": Player_ID},
                )
                conn.commit()
                logger.info(
                    f"{CharacterName} was the players last character also deleted player info"
                )

        logger.info(f"{CharacterName} had {result.rowcount}  rows matched for deletion")

        return "Deleted: " + str(result.rowcount)

    except exc.StatementError as sqlstatementerr:
        logger.exception(sqlstatementerr)
    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
        return Response(status=400, response=f"SQL Error: {sqlerror}")
    except Exception as e:
        logger.exception(e)
        return Response(status=500, response="Error deleting player")


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


if __name__ == "__main__":
    # CharacterName = "Businessman"
    # with db.connect() as conn:
    #     Player_ID = conn.execute(sqlalchemy.text(
    #         """SELECT idPlayers FROM player
    #         JOIN `character` c ON c.Player_idPlayers = idPlayers
    #         WHERE CharacterName = :characterName"""),
    #         {"characterName": CharacterName}).one_or_none()
    #     if Player_ID == None:
    #         last_player = conn.execute(sqlalchemy.text(
    #             f"""SELECT Player_idPlayers FROM `character`
    #             JOIN player ON idPlayers = Player_idPlayers
    #             WHERE Player_idPlayers = 18
    #             """
    #         )).all()
    #     else:
    #         last_player = conn.execute(sqlalchemy.text(
    #             f"""SELECT Player_idPlayers FROM `character`
    #             JOIN player ON idPlayers = Player_idPlayers
    #             WHERE Player_idPlayers = {Player_ID[0]}
    #             """
    #         )).all()

    #     print(f"items found: {last_player}")
    #     print(f"length of items: {len(last_player)}")

    # r = read_current_players_db()
    # for item in r:
    #     print(item)

    players = create_dict_from_db()
    print(players)
