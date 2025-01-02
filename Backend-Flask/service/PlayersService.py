import logging

from sqlalchemy import exc


from utils import customexceptions
from sqlconnector.sqlReader import player_entry
from datagatherer.playerdata import (
    db_find_player_by_name,
    db_find_player_id,
    db_get_character_for_player,
    get_all_players,
    delete_player_from_db,
    delete_char_from_db,
)


logger = logging.getLogger(f"main.{__name__}")

# Informational items
schema = {
    "playerName": str,
    "characterName": str,
    "className": str,
    "role": list[str],
    "combat_roles": dict[str, str],
}


# Processing front end data to fit our sql functions
def process_player_data(incoming_data: dict) -> bool:
    logger.debug(incoming_data)
    new_player = incoming_data.copy()
    new_player.pop("roles")

    roles_list = []
    combat_roles = {}

    for role, details in incoming_data["roles"].items():
        logger.debug(f"role item: {role}:{details}")
        if details.get("enabled") == True:
            roles_list.append(role.lower())
            combat_roles[f"combat_role_{role}"] = details.get("combatRole")
            combat_roles[f"{role}Skill"] = details.get("skill")

    new_player["role"] = roles_list
    logger.debug(f"New player dictionary:\n{new_player}")
    logger.debug(f"New player combat_roles:\n{combat_roles}")

    try:
        result = player_entry(
            **new_player,
            combat_roles=combat_roles,
        )
        return result
    except Exception as e:
        logger.error(e)
        raise customexceptions.DatabaseError("An error occurred adding player")


def process_data_to_frontend(flattened: bool = False):
    """Gets the data from the database and transforms it into a format for use by the front end. Can returned nested data or flatened data depending on needs from the front end"""
    logger.info("gather all players ...")
    try:
        player_entries, char_entries, role_entries = get_all_players()

        # add results to dictionary and create a value of type dict as the entry for that key
        player_dict = {}
        for row in player_entries:
            player_dict[row[1]] = {}

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

        role_dict = {}

        for name, role_type, character, skill in role_entries:
            if name not in role_dict:
                role_dict[name] = {"Roles": []}

            role_dict[name]["Roles"].append({"Type": role_type, "Skill": skill})

        logger.debug(role_dict)

        for key, value in role_dict.items():
            for k, v in player_dict.items():
                if key in v:
                    logger.debug(f"if Key:{player_dict[k][key]}   VALUE : {value}")
                    player_dict[k][key].update(value)
        logger.debug(player_dict)
        logger.info("Gathered all players")

        if flattened:
            flattened_data = []
            for player_name, characters in player_dict.items():
                for char_name, details in characters.items():
                    logger.debug(details)
                    roles_list = []
                    roles_skill = []
                    for roles in details["Roles"]:
                        logger.debug(roles)
                        roles_list.append(roles["Type"])
                        roles_skill.append(roles["Skill"])
                    flattened_data.append(
                        {
                            "Player": player_name,
                            "Character": char_name,
                            "Class": details["Class"],
                            "Dungeon": details["Dungeon"],
                            "Key Level": details["Key Level"],
                            "Range": details["Range"],
                            "Role Type": roles_list,
                            "Role Skill": roles_skill,
                            "Skill Level": details["Skill Level"],
                            "Is Active": details["is_active"],
                        }
                    )
            logger.debug(flattened_data)
            return flattened_data
        return player_dict

    except exc.SQLAlchemyError as e:
        logger.error(e)
        raise customexceptions.DatabaseError("A database error occurred")

    except Exception as e:
        logger.error(e)
        raise Exception from e


def get_player_by_name(player_name: str):
    try:
        data = db_find_player_by_name(player_name)
        if not data:
            raise customexceptions.DataNotFoundError(input=player_name)

        player_data = {"id": data[0], "player name": data[1]}
        return player_data
    except customexceptions.DataNotFoundError as e:
        logger.warning(e)
        raise
    except exc.SQLAlchemyError as e:
        logger.error(e)
        raise customexceptions.DatabaseError
    except Exception as e:
        logger.error(e)
        raise


def delete_player_by_id_or_name(id: str | int):
    try:
        id = int(id)
        player_id, name = db_find_player_id(id)
        logger.debug(f"results of findplayerbyid: {player_id}, {name}")
        if not name:
            print("no data found")
            raise customexceptions.DataNotFoundError(input=id)
    except ValueError:
        logger.debug("id is not a number")
        name = None

    if type(id) not in [int, str]:
        raise TypeError("incorrect type")

    try:
        if not name:
            name = id

        result = delete_player_from_db(name)
        if result:
            return result
        else:
            raise customexceptions.DataNotFoundError(input=id)
    except customexceptions.DataNotFoundError:
        raise
    except exc.SQLAlchemyError as sqlerror:
        logger.error(sqlerror)
        raise customexceptions.DatabaseError
    except Exception as e:
        logger.error(e)
        raise Exception from e


def get_all_chars_from_player(player_name: str):
    try:
        result = db_get_character_for_player(player_name)
        logger.debug(f"result is: {result}")
        if not result:
            raise customexceptions.DataNotFoundError(input=player_name)

        data = {}
        for (
            player_name,
            char_name,
            class_type,
            party_role,
            range_role,
            skill,
            dungeon_name,
            key_level,
            is_active,
        ) in result:
            if char_name in data:
                data[char_name]["party role"].append(party_role)
            else:
                data[char_name] = {
                    # "player name": player_name,
                    "character name": char_name,
                    "class": class_type,
                    "skill": skill,
                    "party role": [party_role],  # Initialize as a list
                    "ranged": range_role,
                    "dungeon": dungeon_name,
                    "key level": key_level,
                    "active": is_active,
                }

        # Convert the dictionary to a list of dictionaries
        data_list = list(data.values())
        logger.debug(f"data is: {data_list}")
        return data_list

    except customexceptions.DataNotFoundError:
        raise
    except exc.SQLAlchemyError as sqlerror:
        logger.error(sqlerror)
        raise customexceptions.DatabaseError
    except Exception as e:
        logger.error(e)
        raise Exception from e


def del_char(character_name: str):
    try:
        result = delete_char_from_db(character_name)
        return result
    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
        raise customexceptions.DatabaseError
