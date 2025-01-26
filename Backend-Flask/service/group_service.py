"""Module is responsible for handling the business logic of the groups creation process."""

import logging

from mythicgroupmaker import create_groups


logger = logging.getLogger(f"main.{__name__}")


def create_groups_service(data):
    """Create groups based on the data provided."""
    logger.debug("Creating groups with: %s", data)
    logger.debug("length of data: %s", len(data))
    logger.debug("type of data: %s", type(data))
    if len(data) < 5:
        logger.warning("Not enough data to create groups")
        return [], []

    groups_list, extra_players_list = create_groups(data)

    if len(groups_list) < 1:
        logger.warning("No groups formed")
        return ([], extra_players_list)

    try:
        for group in groups_list:
            logger.debug("Group: %s", group)
            group_dict = {group.group_number: {}}

            for player in group.group_members:
                p_dict = {player.char_name: dict(player)}
                group_dict[group.group_number].update(p_dict)

        logger.debug("Group dict: %s", group_dict)

    except Exception as e:
        logger.exception(e)
    return group_dict, extra_players_list
