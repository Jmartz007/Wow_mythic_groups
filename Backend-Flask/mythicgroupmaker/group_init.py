import logging


from sqlconnector.sqlReader import (
    create_dict_from_db,
    read_active_players,
)
from . import MythPlayer, GroupPools


logger = logging.getLogger(f"main.{__name__}")


def main(data):
    logger.info("Importing dictionary ... ...")
    player_entries, char_entries, role_entries = read_active_players(data)

    playersDB = create_dict_from_db(is_active=True)
    MythPlayersList = MythPlayer.generate_players_and_chars(playersDB)


    p = GroupPools.Pools(MythPlayersList)
    p.tank_pool()
    p.healer_pool()
    p.dps_pool()
    p.max_groups()

    groupsList = GroupPools.AddMembers.get_tanks(p)

    GroupPools.AddMembers.get_healer(p, groupsList)

    GroupPools.AddMembers.get_dps(p, groupsList)
    print(groupsList)
    # logger.debug("players left:\n" + str(players_list))
    logger.debug("players left:\n" + str(MythPlayersList))
    logger.debug("Max groups: " + str(p.maxGroups))
    logger.info("created groupsList")
    logger.debug(print(groupsList))
    return groupsList, MythPlayersList
