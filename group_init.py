# from player_generator import new_dict
from mythic_groups_maker import *
from sqlconnector.sqlReader import create_dict_from_db
import logging

logger = logging.getLogger()


def main():
    sqlPlayerDict = create_dict_from_db()
    logger.info("Importing dictionary ... ...")
    importedDict = sqlPlayerDict
    logger.debug(importedDict)

    players_list = players_gen(sqlPlayerDict)

    p = Pools(players_list)
    p.tank_pool()
    p.healer_pool()
    p.dps_pool()
    p.max_groups()

    groupsList = AddMembers.get_tanks(p)

    print_all_players(players_list)
    print(len(players_list))

    AddMembers.get_healer(p, groupsList)

    print(players_list)
    print(len(players_list))
    print("\n")

    AddMembers.get_dps(p, groupsList)
    print(groupsList)
    logger.debug("players left:\n" + str(players_list))
    logger.debug("Max groups: " + str(p.maxGroups))
    logger.info("created groupsList")
    logger.debug(print(groupsList))
    return groupsList

# need to fix 3 players remaining when there should be 0