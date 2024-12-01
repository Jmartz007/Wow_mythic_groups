import logging

import sqlalchemy
from sqlalchemy import exc

if __name__ == "__main__":
    from sqlconnector.connect_localconnection import local_conn

    db = local_conn()

else:
    from sqlconnector.connection_pool import init_connection_pool

    db = init_connection_pool()

logger = logging.getLogger(f"main.{__name__}")


def get_all_players(is_active: bool = False):
    """
    Does a database query to get all players and related data. Optinally can get active players only.

    Args:
        is_active (bool): True gets active players only

    Returns:
        tuple: player_entries, char_entries, role_entries
    """
    with db.connect() as conn:
        if is_active:
            player_entries = conn.execute(
                sqlalchemy.text(
                    f"""SELECT p.idPlayers, p.PlayerName
                    FROM player p
                    JOIN `character` `c` on p.idPlayers = `c`.Player_idPlayers
                    WHERE  `c`.is_active = 1"""
                )
            ).fetchall()
            char_entries = conn.execute(
                sqlalchemy.text(
                    f"""SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                    FROM char_info
                    WHERE is_active = 1"""
                )
            ).fetchall()
        else:
            player_entries = conn.execute(
                sqlalchemy.text(f"SELECT * FROM player")
            ).fetchall()
            char_entries = conn.execute(
                sqlalchemy.text(
                    f"""SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                    FROM char_info"""
                )
            ).fetchall()
        logger.debug(char_entries)
        logger.info("Query from tables (players, characters) executed successfully")

        role_entries = conn.execute(
            sqlalchemy.text(
                f"""SELECT c.CharacterName, pr.PartyRoleName, c.ClassName, cr.RoleSkill FROM `character` as c
            JOIN combatrole_has_character AS cr ON cr.Character_idCharacter = c.idCharacter
            JOIN partyrole AS pr ON pr.idPartyRole = cr.PartyRole_idPartyRole
            """
            )
        ).fetchall()
        logger.info(
            "Query from tables (character, combatrole_has_character, partyrole) executed successfully"
        )

    return player_entries, char_entries, role_entries
