# from player_generator import new_dict
from .mythic_groups_maker import *
from sqlconnector.sqlReader import create_dict_from_db, read_active_players, create_player_dict
import logging

logger = logging.getLogger(f"main.{__name__}")


def main(data):
    logger.info("Importing dictionary ... ...")
    # sqlPlayerDict = create_dict_from_db()
    player_entries, char_entries, role_entries = read_active_players(data)
    sqlPlayerDict = create_player_dict(player_entries, char_entries, role_entries)
    logger.debug(sqlPlayerDict)

    players_list = players_gen(sqlPlayerDict)

    p = Pools(players_list)
    p.tank_pool()
    p.healer_pool()
    p.dps_pool()
    p.max_groups()

    groupsList = AddMembers.get_tanks(p)

    AddMembers.get_healer(p, groupsList)

    AddMembers.get_dps(p, groupsList)
    print(groupsList)
    logger.debug("players left:\n" + str(players_list))
    logger.debug("Max groups: " + str(p.maxGroups))
    logger.info("created groupsList")
    logger.debug(print(groupsList))
    return groupsList, players_list
