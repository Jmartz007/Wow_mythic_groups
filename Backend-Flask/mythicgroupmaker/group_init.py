import logging


# from sqlconnector.sqlReader import create_dict_from_db
from datagatherer.group_data import read_active_players, create_dict_from_db
from . import MythPlayer, GroupPools


logger = logging.getLogger(f"main.{__name__}")


def main(data):
    """The main function which creates groups from the dictionary of active players provided."""
    logger.info("Creating Groups ... ...")
    results_tuple = read_active_players(data)

    players_db = create_dict_from_db(is_active=True)
    myth_players_list = MythPlayer.generate_players_and_chars(players_db)

    p = GroupPools.Pools(myth_players_list)
    p.tank_pool()
    p.healer_pool()
    p.dps_pool()
    p.max_groups()

    groups_list = GroupPools.AddMembers.get_tanks(p)

    GroupPools.AddMembers.get_healer(p, groups_list)

    GroupPools.AddMembers.get_dps(p, groups_list)
    logger.debug(groups_list)
    # logger.debug("players left:\n" + str(players_list))
    logger.debug("players left: %s", str(myth_players_list))
    logger.debug("Max groups: %s", str(p.maxGroups))
    logger.info("created groupsList")
    logger.debug(groups_list)
    return groups_list, myth_players_list
