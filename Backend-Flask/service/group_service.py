"""Module is responsible for handling the business logic of the groups creation process."""

import logging

from mythicgroupmaker import create_groups


logger = logging.getLogger(f"main.{__name__}")


def create_groups_service(data):
    """Create groups based on the data provided."""
    logger.debug("Creating groups with: %s", data)
    groups_list, extra_players_list = create_groups(data)
    for group in groups_list:
        logger.debug("Group: %s", group)

    return groups_list, extra_players_list
