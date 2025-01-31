"""Module is responsible for handling the business logic of the groups creation process."""

import logging

from mythicgroupmaker import create_groups
from utils.customexceptions import ServiceException


logger = logging.getLogger(f"main.{__name__}")


def create_groups_service(data):
    """Create groups based on the data provided."""
    logger.debug("Creating groups with: %s", data)
    logger.debug("length of data: %s", len(data))
    logger.debug("type of data: %s", type(data))
    try:
        if len(data) < 5:
            logger.warning("Not enough data to create groups")
            raise ServiceException("Must select at least 5 players to create groups")

        groups_list, extra_players_list = create_groups(data)

        if len(groups_list) < 1:
            logger.warning("No groups formed")
            raise ServiceException("Could not form groups from the selected players")

        for group in groups_list:
            logger.debug("Group: %s", group)
            group_dict = {group.group_number: {}}

            for player in group.group_members:
                p_dict = {player.char_name: dict(player)}
                group_dict[group.group_number].update(p_dict)

        logger.debug("Group dict: %s", group_dict)

    except ServiceException as e:
        logger.error(e)
        raise ServiceException(e)

    return group_dict, extra_players_list
