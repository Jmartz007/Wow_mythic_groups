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
                    """SELECT p.idPlayers, p.PlayerName
                    FROM Player p
                    JOIN `Character` `c` on p.idPlayers = `c`.Player_idPlayers
                    WHERE  `c`.is_active = 1"""
                )
            ).fetchall()
            char_entries = conn.execute(
                sqlalchemy.text(
                    """SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                    FROM char_info
                    WHERE is_active = 1"""
                )
            ).fetchall()
        else:
            player_entries = conn.execute(
                sqlalchemy.text("SELECT * FROM Player")
            ).fetchall()
            char_entries = conn.execute(
                sqlalchemy.text(
                    """SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level, is_active
                    FROM char_info"""
                )
            ).fetchall()
        logger.debug(char_entries)
        logger.info("Query from tables (players, characters) executed successfully")

        role_entries = conn.execute(
            sqlalchemy.text(
                """SELECT c.CharacterName, pr.PartyRoleName, c.ClassName, cr.RoleSkill
                FROM `Character` as c
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
        "Deleted %s and %s characters associated", PlayerName, char_result.rowcount
    )
    return player_result.rowcount


def handle_combat_role(conn, role_type, role_id, charID, characterName, combat_roles):
    """Function to apply the appropriate range for a character's combat role."""
    range_id = (
        lambda x: (
            1
            if x.get(f"combat_role_{role_type}") == "Melee"
            else 2 if x.get(f"combat_role_{role_type}") == "Ranged" else None
        )
    )(combat_roles)
    logger.debug("%s rangeID: %s", role_type.capitalize(), range_id)
    try:
        conn.execute(
            sqlalchemy.text(
                """REPLACE INTO `CombatRole_has_Character`
                (`RoleRange_idRoleRange`, `Character_idCharacter`, `PartyRole_idPartyRole`, `RoleSkill`)
                SELECT :range, idCharacter, :role_id, :skill FROM `Character`
                WHERE CharacterName = :characterName"""
            ),
            {
                "range": range_id,
                "characterName": characterName,
                "role_id": role_id,
                "skill": combat_roles[f"{role_type}Skill"],
            },
        )
        conn.execute(
            sqlalchemy.text(
                """DELETE FROM `CombatRole_has_Character` WHERE (`PartyRole_idPartyRole` = :role_id)
                AND (`Character_idCharacter` = :charID)
                AND (`RoleRange_idRoleRange` != :range)"""
            ),
            {"charID": charID, "range": range_id, "role_id": role_id},
        )
    except exc.IntegrityError as e:
        logger.error(e)
        raise


def player_entry(
    player_name: str,
    characterName: str,
    className: str,
    role: list[str],
    combat_roles: dict[str, str],
    **kwargs,
):
    """Function to insert a player and character into the database."""
    dungeon = kwargs.get("dungeon", "Unknown")
    keylevel = kwargs.get("keylevel")
    try:
        with db.connect() as conn:
            # insert player
            id_players = conn.execute(
                sqlalchemy.text(
                    "SELECT idPlayers PlayerName FROM Player WHERE PlayerName=:playerName"
                ),
                {"playerName": player_name},
            ).first()
            if not id_players:
                conn.execute(
                    sqlalchemy.text(
                        "INSERT INTO Player (PlayerName) VALUES (:playerName)"
                    ),
                    {"playerName": player_name},
                )
                id_players = conn.execute(
                    sqlalchemy.text(
                        "SELECT idPlayers, PlayerName FROM Player WHERE PlayerName=:playerName"
                    ),
                    {"playerName": player_name},
                ).first()
                logger.debug("Adding %s to database", player_name)
            else:
                logger.debug("%s exists", player_name)
            player_id = id_players[0]

            # insert character and mythic key
            stmt = sqlalchemy.text(
                "SELECT * FROM `Character` WHERE CharacterName = :charName"
            )
            result = conn.execute(stmt, {"charName": characterName}).first()
            if result:
                logger.info("character %s already exists", characterName)
            elif not result:
                logger.info("adding character %s", characterName)

                insert_mythic_key_stmt = sqlalchemy.text(
                    """INSERT INTO `MythicKey` (`level`, `Dungeon_id`)
                    SELECT :keylevel, idDungeon FROM `Dungeon`
                    WHERE DungeonName = :dungeon"""
                )
                logger.debug(keylevel)
                logger.debug(dungeon)
                insert_result = conn.execute(
                    insert_mythic_key_stmt,
                    {
                        "keylevel": keylevel,
                        "dungeon": dungeon,
                    },
                ).rowcount
                logger.debug("inserted %s rows into MythicKey", insert_result)

                mythic_key_id = conn.execute(
                    sqlalchemy.text("SELECT LAST_INSERT_ID()")
                ).scalar()
                logger.debug("mythic_key_id or last_insert_id: %s", mythic_key_id)

                insert_character_stmt = sqlalchemy.text(
                    """INSERT INTO `Character`
                    (`CharacterName`, `ClassName`, `PlayerRating`, `Player_idPlayers`, `MythicKey_id`)
                    VALUES
                    (:characterName, :className, 'Intermediate', :playerID, :mythicKeyID)"""
                )
                conn.execute(
                    insert_character_stmt,
                    {
                        "characterName": characterName,
                        "className": className,
                        "playerID": player_id,
                        "mythicKeyID": mythic_key_id,
                    },
                )
                conn.commit()
                result = conn.execute(stmt, {"charName": characterName}).first()
                logger.debug(result)

            char_id = result[0]
            mythic_key_id = result[4]
            logger.debug("MythicKey_id: %s", mythic_key_id)

            for role_type, role_id in [("tank", 2), ("healer", 1), ("dps", 3)]:
                if role_type in role:
                    handle_combat_role(
                        conn, role_type, role_id, char_id, characterName, combat_roles
                    )
                else:
                    logger.info("removing %s role, not selected", role_type)
                    conn.execute(
                        sqlalchemy.text(
                            """DELETE FROM `CombatRole_has_Character`
                            WHERE (`PartyRole_idPartyRole` = :role_id)
                            and (`Character_idCharacter` = :charID)"""
                        ),
                        {"charID": char_id, "role_id": role_id},
                    )

            conn.commit()

    except exc.SQLAlchemyError as error:
        logger.exception(error)
        raise error
    except Exception as e:
        logger.exception(e)
        raise e

    logger.info("Entry successful for '%s'", player_name)
    return True


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
    """Database function which deletes a character from the database."""
    with db.connect() as conn:

        player_id = conn.execute(
            sqlalchemy.text(
                """SELECT idPlayers FROM Player
            JOIN `Character` c ON c.Player_idPlayers = idPlayers
            WHERE CharacterName = :characterName"""
            ),
            {"characterName": CharacterName},
        ).one()

        player_id = player_id[0]

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
            WHERE Player_idPlayers = {player_id} 
            """
            )
        ).all()
        logger.debug(last_player)
        logger.debug(len(last_player))
        if len(last_player) == 0:
            conn.execute(
                sqlalchemy.text(
                    """
                    DELETE FROM `Player`
                    WHERE `Player`.`idPlayers` = :playerID;
                    """
                ),
                {"playerID": player_id},
            )
            conn.commit()
            logger.info(
                "%s was the player's last character also deleted player info",
                CharacterName,
            )

            logger.info(
                "%s had %s rows matched for deletion", CharacterName, result.rowcount
            )

    return result.rowcount
