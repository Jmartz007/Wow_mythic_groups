from ast import Dict
import logging

import sqlalchemy
from sqlalchemy import exc


import utils.customexceptions
from sqlconnector.sqlReader import create_dict_from_db, player_entry
from datagatherer import getplayers


logger = logging.getLogger(f"main.{__name__}")

# Informational items
example_data = {
    "playerName": "Fern",
    "characterName": "Fernicus",
    "dungeon": "City of Threads",
    "keylevel": 0,
    "class": "Warrior",
    "roles": {
        "tank": {"enabled": False, "skill": 0, "combatRole": ""},
        "healer": {"enabled": False, "skill": 0, "combatRole": ""},
        "dps": {"enabled": True, "skill": 0, "combatRole": "Melee"},
    },
}
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
        logger.error("an error occurred adding player")
        return False


def process_data_to_frontend(flattened: bool = False):
    """Gets the data from the database and transforms it into a format for use by the front end. Can returned nested data or flatened data depending on needs from the front end"""
    logger.info("gather all players ...")
    try:
        player_entries, char_entries, role_entries = getplayers.get_all_players()

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
            # Flattening the data to send to the front end
            flattened_data = []
            for player_name, characters in player_dict.items():
                for char_name, details in characters.items():
                    for roles in details["Roles"]:
                        flattened_data.append(
                            {
                                "Player": player_name,
                                "Character": char_name,
                                "Class": details["Class"],
                                "Dungeon": details["Dungeon"],
                                "Key Level": details["Key Level"],
                                "Range": details["Range"],
                                "Role Type": roles["Type"],
                                "Role Skill": roles["Skill"],
                                "Skill Level": details["Skill Level"],
                                "Is Active": details["is_active"],
                            }
                        )
            return flattened_data

        return player_dict

    except exc.SQLAlchemyError as e:
        logger.error(e)
        raise utils.customexceptions.DatabaseError("A database error occurred")
