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


def db_find_player_id(player_id: int):
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                """SELECT p.idPlayers, p.PlayerName
            FROM Player p
            WHERE p.idPlayers = :playerid"""
            ),
            {"playerid": player_id},
        ).one_or_none()

    return result


def db_find_player_by_name(player_name: str):
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                """
                SELECT p.idPlayers, p.PlayerName
                FROM Player p
                WHERE p.PlayerName = :playername
                """
            ),
            {"playername": player_name},
        ).one_or_none()

    return result


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
                    FROM Player p
                    JOIN `Character` `c` on p.idPlayers = `c`.Player_idPlayers
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
                sqlalchemy.text(f"SELECT * FROM Player")
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
                f"""SELECT c.CharacterName, pr.PartyRoleName, c.ClassName, cr.RoleSkill FROM `Character` as c
            JOIN CombatRole_has_Character AS cr ON cr.Character_idCharacter = c.idCharacter
            JOIN PartyRole AS pr ON pr.idPartyRole = cr.PartyRole_idPartyRole
            """
            )
        ).fetchall()
        logger.info(
            "Query from tables (Character, CombatRole_has_Character, PartyRole) executed successfully"
        )

    return player_entries, char_entries, role_entries


def delete_player_from_db(PlayerName: str):
    """
    Deletes a player and associated characters from the database.

    Args:
        PlayerName (str): The player to be deleted from the database.

    Returns:
        rowcount (int): The number of rows deleted in the player table.
    """
    with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                """
            DELETE FROM `CombatRole_has_Character`
            WHERE `Character_idCharacter` IN (
                SELECT idCharacter FROM `Character`
                JOIN Player ON idPlayers = Player_idPlayers
                WHERE `Player`.`PlayerName` = :playerName);
            """
            ),
            {"playerName": PlayerName},
        )
        char_result = conn.execute(
            sqlalchemy.text(
                """
            DELETE FROM `Character` 
            WHERE Player_idPlayers IN (
                SELECT idPlayers FROM `Player`
                WHERE `Player`.`PlayerName` = :playerName);
            """
            ),
            {"playerName": PlayerName},
        )
        player_result = conn.execute(
            sqlalchemy.text(
                """
            DELETE FROM `Player`
            WHERE `Player`.`PlayerName` = :playerName;
            """
            ),
            {"playerName": PlayerName},
        )
        conn.commit()
    logger.info(
        f"Deleted {PlayerName} and {char_result.rowcount} characters associated"
    )
    return player_result.rowcount


def db_get_character_for_player(player_name: str) -> list[tuple]:
    """
    Gets all characters for a player.

    Args:
        player_name (str): The player to get characters for.

    Returns:
        result (list): The characters for the player.
    """
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                """
                SELECT `char_info`.`PlayerName`,
                    `char_info`.`CharacterName`,
                    `char_info`.`ClassName`,
                    `char_info`.`PartyRoleName`,
                    `char_info`.`RoleRangeName`,
                    `char_info`.`RoleSkill`,
                    `char_info`.`DungeonName`,
                    `char_info`.`level`,
                    `char_info`.`is_active`
                FROM `char_info`
                WHERE `char_info`.`PlayerName` = :playername
                """
            ),
            {"playername": player_name},
        ).fetchall()

    return result


def db_find_character_by_name(character_name: str):
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                """
                SELECT idCharacter,
                    CharacterName,
                    ClassName,
                    PlayerRating,
                    MythicKey_id,
                    Player_idPlayers,
                    is_active
                FROM `Character`
                WHERE CharacterName = :charactername
                """
            ),
            {"charactername": character_name},
        ).one_or_none()

    return result


def db_get_all_info_for_character(character_name: str):
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(
                """
                SELECT `char_info`.`PlayerName`,
                    `char_info`.`CharacterName`,
                    `char_info`.`ClassName`,
                    `char_info`.`is_active`,
                    `char_info`.`PartyRoleName`,
                    `char_info`.`RoleRangeName`,
                    `char_info`.`RoleSkill`,
                    `char_info`.`DungeonName`,
                    `char_info`.`level`
                FROM `mythicsdb`.`char_info`
                WHERE `char_info`.`CharacterName` = :charactername
                """
            ),
            {"charactername": character_name},
        ).fetchall()

    return result


def delete_char_from_db(CharacterName: str):
    """"""
    with db.connect() as conn:

        Player_ID = conn.execute(
            sqlalchemy.text(
                """SELECT idPlayers FROM Player
            JOIN `Character` c ON c.Player_idPlayers = idPlayers
            WHERE CharacterName = :characterName"""
            ),
            {"characterName": CharacterName},
        ).one()

        Player_ID = Player_ID[0]

        conn.execute(
            sqlalchemy.text(
                """DELETE FROM `CombatRole_has_Character`
            WHERE `Character_idCharacter` IN (
            SELECT idCharacter FROM `Character`
            WHERE `Character`.`CharacterName` = :characterName)"""
            ),
            {"characterName": CharacterName},
        )
        result = conn.execute(
            sqlalchemy.text(
                """DELETE FROM `Character`
            WHERE `CharacterName` = :characterName"""
            ),
            {"characterName": CharacterName},
        )

        conn.commit()

        last_player = conn.execute(
            sqlalchemy.text(
                f"""SELECT Player_idPlayers FROM `Character`
            JOIN Player ON idPlayers = Player_idPlayers
            WHERE Player_idPlayers = {Player_ID} 
            """
            )
        ).all()
        logger.debug(last_player)
        logger.debug(len(last_player))
        if len(last_player) == 0:
            player_del = conn.execute(
                sqlalchemy.text(
                    """
            DELETE FROM `Player`
            WHERE `Player`.`idPlayers` = :playerID;
            """
                ),
                {"playerID": Player_ID},
            )
            conn.commit()
            logger.info(
                f"{CharacterName} was the player's last character also deleted player info"
            )

    logger.info(f"{CharacterName} had {result.rowcount}  rows matched for deletion")

    return result.rowcount
