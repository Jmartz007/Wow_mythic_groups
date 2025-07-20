"""This module contains database functions related to data needed to create groups."""

import logging

import sqlalchemy
from sqlalchemy import exc

from sqlconnector.connection_pool import init_connection_pool


logger = logging.getLogger(f"main.{__name__}")

db = init_connection_pool()


def read_active_players(is_active: dict):
    """Makes the players active in the database and switches the rest to inactive.

    Args:
        is_active (dict): A dictionary of players to make active

    Returns:
        player_entries (tuple): A list of players that are active
        char_entries (tuple): A list of characters that are active
        role_entries (tuple): A list of roles for the characters"""
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

            # Execute the query and fetch all results
            player_entries = conn.execute(
                sqlalchemy.text(
                    """SELECT p.idPlayers, p.PlayerName
                        FROM player p
                        JOIN `character` `c` on p.idPlayers = `c`.Player_idPlayers
                        WHERE  `c`.is_active = 1"""
                )
            ).fetchall()

            char_entries = conn.execute(
                sqlalchemy.text(
                    """SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                    FROM char_info
                    WHERE is_active = 1
                    """
                )
            ).fetchall()
            logger.debug(char_entries)
            logger.info("Query from tables (players, characters) executed successfully")

            role_entries = conn.execute(
                sqlalchemy.text(
                    """SELECT c.CharacterName, pr.PartyRoleName, c.ClassName, cr.RoleSkill FROM `character` as c
                    JOIN combatrole_has_character AS cr ON cr.Character_idCharacter = c.idCharacter
                    JOIN partyrole AS pr ON pr.idPartyRole = cr.PartyRole_idPartyRole
                    """
                )
            ).fetchall()
            logger.info(
                "Query from tables (character, combatrole_has_character, partyrole) executed successfully"
            )

            return player_entries, char_entries, role_entries

    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
        raise
    except Exception as error:
        logger.exception(error)
        raise


def create_dict_from_db(is_active: bool = False) -> dict:
    """Retrieves players from the DB and adds them to a dictionary"""
    player_dict = {}
    try:
        with db.connect() as conn:
            # Execute the query and fetch all results

            if is_active:
                player_entries = conn.execute(
                    sqlalchemy.text(
                        """SELECT p.idPlayers, p.PlayerName
                        FROM player p
                        JOIN `character` `c` on p.idPlayers = `c`.Player_idPlayers
                        WHERE  `c`.is_active = 1"""
                    )
                ).fetchall()
                charEntries = conn.execute(
                    sqlalchemy.text(
                        """SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                        FROM char_info
                        WHERE is_active = 1"""
                    )
                ).fetchall()
            else:
                player_entries = conn.execute(
                    sqlalchemy.text("SELECT * FROM player")
                ).fetchall()
                charEntries = conn.execute(
                    sqlalchemy.text(
                        """SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                        FROM char_info"""
                    )
                ).fetchall()
            logger.debug(charEntries)
            logger.info("Query from tables (players, characters) executed successfully")

            roleEntries = conn.execute(
                sqlalchemy.text(
                    """SELECT c.CharacterName, pr.PartyRoleName, c.ClassName, cr.RoleSkill FROM `character` as c
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
        raise ValueError("Could not find player entries") from sqlerror

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
