"""Module is responsible for handling the business logic of the groups creation process."""

import logging

from mythicgroupmaker import create_groups


logger = logging.getLogger(f"main.{__name__}")


def create_groups_service(data):
    """Create groups based on the data provided."""
    logger.debug("Creating groups with: %s", data)
    groups_list, extra_players_list = create_groups(data)
    try:
        for group in groups_list:
            logger.debug("Group: %s", group)
            # group_dict = {"new_group": group}
            # logger.debug("Group dict: %s", group_dict)
            group_dict = {group.group_number: {}}

            for player in group.group_members:
                group_dict[group.group_number].update(player)
                logger.debug("Group dict: %s", group_dict)
                
    except Exception as e:
        logger.exception(e)
    return groups_list, extra_players_list
