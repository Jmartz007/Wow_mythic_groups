import logging
from sqlconnector.sqlReader import player_entry


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
