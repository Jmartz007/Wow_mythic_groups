import logging
from ast import Dict, List, Try
from re import DEBUG

import sqlalchemy
from sqlalchemy import exc
from flask import Response


if __name__=="__main__":
    from connect_localconnection import local_conn
    db = local_conn()
else:
    from .connection_pool import init_connection_pool
    db = init_connection_pool()

logger = logging.getLogger(f"main.{__name__}")

def create_dict_from_db() -> dict:
    '''Retrieves players from the DB and adds them to a dictionary'''
    player_dict = {}
    try:
        with db.connect() as conn:
            # Execute the query and fetch all results
            player_entries = conn.execute(
                sqlalchemy.text( f"SELECT * FROM player" )
            ).fetchall()

            charEntries = conn.execute(
                sqlalchemy.text( f'''SELECT `p`.`PlayerName`, `c`.`CharacterName`, `c`.`ClassName`
            FROM `player` as `p` LEFT JOIN `character` as `c` ON `p`.`idPlayers` = `c`.`Player_idPlayers` ''' )
            ).fetchall()
            charEntries = conn.execute(
                sqlalchemy.text(
                    f"""SELECT PlayerName, CharacterName, ClassName, RoleRangeName, RoleSkill, DungeonName, level
                    FROM char_info"""
                )
            ).fetchall()
            logger.debug(charEntries)
            logger.info("Query from tables (players, characters) executed successfully")

            roleEntries = conn.execute(
                sqlalchemy.text( f'''SELECT c.CharacterName, pr.PartyRoleName, c.ClassName, cr.RoleSkill FROM `character` as c
                JOIN combatrole_has_character AS cr ON cr.Character_idCharacter = c.idCharacter
                JOIN partyrole AS pr ON pr.idPartyRole = cr.PartyRole_idPartyRole
                ''' )
            ).fetchall()
            logger.info("Query from tables (character, combatrole_has_character, partyrole) executed successfully")

        #add results to dictionary and create a value of type dict as the entry for that key
        for row in player_entries:
            player_dict[row[1]] = {}

    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
    except Exception as error:
        logger.exception(error)
  
    # add characters to the player entries
    try:
        for row in charEntries:
            for key, value in player_dict.items():
                if key == row[0] and (len(value)==0):
                    player_dict[row[0]] = {row[1] : {"Class": row[2], "Range": row[3], "Skill Level": row[4], "Dungeon": row[5], "Key Level": row[6]  } }   # <--- where to add a characters information to the 
                elif key == row[0]:
                    player_dict[row[0]].update({row[1]: {"Class": row[2], "Range": row[3], "Skill Level": row[4], "Dungeon": row[5], "Key Level": row[6] } })  # <----------- here too
                else:
                    # print("row did not match key\n")
                    continue
        logger.info("Characters added to players dictionary")
    except Exception as error:
        logger.exception(error)
        
    # add role information to the characters in the dictionary
    try:
        newDict = {}
        for i in roleEntries:
            logger.debug(i)
            # creating a new list to add multiple roles if needed
            newList = []
            if i[0] in newDict.keys():
                if len(newDict[i[0]]["Role"])>=2:
                    newList.extend([newDict[i[0]]["Role"][0], newDict[i[0]]["Role"][1], i[1]])
                    if i[1] == "Tank":
                        newDict[i[0]].update({"Role": newList, "Tank Skill": i[3]})
                    elif i[1] == "Healer":
                        newDict[i[0]].update({"Role": newList, "Healer Skill": i[3]})
                    elif i[1] == "DPS":
                        newDict[i[0]].update({"Role": newList, "DPS Skill": i[3]})
                    continue

                newList.extend([newDict[i[0]]["Role"][0], i[1]])

                if i[1] == "Tank":
                    newDict[i[0]].update({"Role": newList, "Tank Skill": i[3]})
                elif i[1] == "Healer":
                    newDict[i[0]].update({"Role": newList, "Healer Skill": i[3]})
                elif i[1] == "DPS":
                    newDict[i[0]].update({"Role": newList, "DPS Skill": i[3]})

            else:
                newList.append(i[1])
                if i[1] == "Tank":
                    newDict.update({i[0]:{"Role": newList, "Tank Skill": i[3]}})
                elif i[1] == "Healer":
                    newDict.update({i[0]:{"Role": newList, "Healer Skill": i[3]}})
                elif i[1] == "DPS":
                    newDict.update({i[0]:{"Role": newList, "DPS Skill": i[3]}})

        # print(newDict)
        for key, value in newDict.items():
            for k, v in player_dict.items():
                if key in v:
                    player_dict[k][key].update(value)
        logger.debug(player_dict)
        logger.info("sqlReader successfully created dictionary from database")
        
    except Exception as error:
        logger.error(error)

    return player_dict


def read_current_players_db() -> List:
    playerListDB = []
    try:
        with db.connect() as conn:
            results = conn.execute(sqlalchemy.text("SELECT * FROM char_info")).fetchall()
        for row in results:
            playerListDB.append(row)

    except Exception as e:
        logger.exception(e)
        return Response(
            status=500,
            response="Unable to read the players from the DB")
    logger.info("Successfully read the players from the database")
    return playerListDB


def delete_player(PlayerName: str):
    try:
        with db.connect() as conn:
            conn.execute(sqlalchemy.text('''
                DELETE FROM `combatrole_has_character`
                WHERE `Character_idCharacter` IN (
                    SELECT idCharacter FROM `character`
                    JOIN player ON idPlayers = Player_idPlayers
                    WHERE `player`.`PlayerName` = :playerName);
                '''),
                {"playerName": PlayerName}
                )
            conn.execute(sqlalchemy.text('''
                DELETE FROM `character` 
                WHERE Player_idPlayers IN (
                    SELECT idPlayers FROM `player`
                    WHERE `player`.`PlayerName` = :playerName);
                '''),
                {"playerName": PlayerName}
                )
            result = conn.execute(sqlalchemy.text('''
                DELETE FROM `player`
                WHERE `player`.`PlayerName` = :playerName;
                '''),
                {"playerName": PlayerName}
                )
            conn.commit()
        logger.info(f"{result.rowcount}  rows matched for deletion")
        logger.info(f"Deleted {result}")
        return "Deleted: " + str(result.rowcount)

    except exc.StatementError as sqlstatementerr:
        logger.exception(sqlstatementerr)
    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
        return Response(status=400, response=f"SQL Error: {sqlerror}")
    except Exception as e:
        logger.exception(e)
        return Response(status=500, response="Error deleting player")


def delete_character(CharacterName: str):
    try:
        with db.connect() as conn:

            Player_ID = conn.execute(sqlalchemy.text(
                """SELECT idPlayers FROM player
                JOIN `character` c ON c.Player_idPlayers = idPlayers
                WHERE CharacterName = :characterName"""),
                {"characterName": CharacterName}).one()
            
            Player_ID = Player_ID[0]

            conn.execute(sqlalchemy.text(
                """DELETE FROM `combatrole_has_character`
                WHERE `Character_idCharacter` IN (
                SELECT idCharacter FROM `character`
                WHERE `character`.`CharacterName` = :characterName)"""),
                {"characterName": CharacterName})
            result = conn.execute(sqlalchemy.text(
                """DELETE FROM `character`
                WHERE `CharacterName` = :characterName"""),
                {"characterName": CharacterName})

            conn.commit()

            last_player = conn.execute(sqlalchemy.text(
                f"""SELECT Player_idPlayers FROM `character`
                JOIN player ON idPlayers = Player_idPlayers
                WHERE Player_idPlayers = {Player_ID} 
                """
                )).all()
            print(last_player)
            print(len(last_player))
            if len(last_player) == 0:
                player_del = conn.execute(sqlalchemy.text('''
                DELETE FROM `player`
                WHERE `player`.`idPlayers` = :playerID;
                '''),
                {"playerID": Player_ID})
                conn.commit()
                logger.info(f"No of player rows deleted: {player_del.rowcount}")


        logger.info(f"{result.rowcount}  rows matched for deletion")

        return "Deleted: " + str(result.rowcount)

    except exc.StatementError as sqlstatementerr:
        logger.exception(sqlstatementerr)
    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
        return Response(status=400, response=f"SQL Error: {sqlerror}")
    except Exception as e:
        logger.exception(e)
        return Response(status=500, response="Error deleting player")


def player_entry(playerName: str, characterName: str, className: str, role: list[str], combat_roles: dict[str, str], **kwargs):
    dungeon = kwargs.get("dungeon")
    keylevel = kwargs.get("keylevel")
    try:
        # Using a with statement ensures that the connection is always released
        # back into the pool at the end of statement (even if an error occurs)
        with db.connect() as conn:
            # insert player
            id = conn.execute(sqlalchemy.text("SELECT idPlayers PlayerName FROM player WHERE PlayerName=:playerName"),
                {"playerName": playerName}).first()

            if not id:
                conn.execute(sqlalchemy.text("INSERT INTO player (PlayerName) VALUES (:playerName)"), 
                             {"playerName": playerName})
                id = conn.execute(sqlalchemy.text("SELECT idPlayers, PlayerName FROM player WHERE PlayerName=:playerName"),
                             {"playerName": playerName}).first()
            playerID = id[0]
                

            # insert character
            stmt = sqlalchemy.text("SELECT * FROM `character` WHERE CharacterName = :charName")
            result = conn.execute(stmt, {"charName": characterName}).first()
            if result:
                logger.info(f"character {characterName} already exists")
            elif not result:
                logger.info(f"adding character {characterName}")
                insert_stmt = sqlalchemy.text(
                    """INSERT INTO `character`
                    (`CharacterName`, `ClassName`, `PlayerRating`,`Player_idPlayers`)
                    VALUES
                    (:characterName, :className, 'Intermediate', :playerID)""")

                conn.execute(insert_stmt, {"characterName": characterName, "className": className, "playerID": playerID})
                conn.commit()
                result = conn.execute(stmt, {"charName": characterName}).first()
                logger.debug(result)

            charID = result[0]
            Id_Mythic_Key = result[4]
            logger.debug(f"MythicKey_id: {Id_Mythic_Key}")

            for i in role:
                if  i == "Tank":
                    tankrange_id = (lambda x: 1 if x.get("combat_role_tank") == "Melee" else 2 if x.get("combat_role_tank") == "Ranged" else None)(combat_roles)
                    logger.debug(f"Tank rangeID: {tankrange_id}")
                    try:
                        conn.execute(sqlalchemy.text(
                            """REPLACE INTO `combatrole_has_character`
                            (`RoleRange_idRoleRange`,
                            `Character_idCharacter`,
                            `PartyRole_idPartyRole`,
                            `RoleSkill`)
                            SELECT :range, idCharacter, 2, :skill FROM `character`
                            WHERE CharacterName = :characterName"""
                        ),
                        {"range": tankrange_id, "characterName": characterName, "skill": combat_roles["tankSkill"]})

                        conn.execute(sqlalchemy.text(
                            """DELETE FROM `combatrole_has_character` WHERE (`PartyRole_idPartyRole` = '2')
                            AND (`Character_idCharacter` = :charID)
                            AND (`RoleRange_idRoleRange` != :range)"""), {"charID": charID, "range": tankrange_id}
                        )
                    except exc.IntegrityError as e:
                        logger.warning(e)

                elif i == "Healer":
                    healerrange_id = (lambda x: 1 if x.get("combat_role_healer") == "Melee" else 2 if x.get("combat_role_healer") == "Ranged" else None)(combat_roles)
                    logger.debug(f"healer rangeID: {healerrange_id}")
                    try:
                        conn.execute(sqlalchemy.text(
                            """REPLACE INTO `combatrole_has_character`
                            (`RoleRange_idRoleRange`,
                            `Character_idCharacter`,
                            `PartyRole_idPartyRole`,
                            `RoleSkill`)
                            SELECT :range, idCharacter, 1, :skill FROM `character`
                            WHERE CharacterName = :characterName"""
                        ),
                        {"range": healerrange_id, "characterName": characterName, "skill": combat_roles["healerSkill"]})

                        conn.execute(sqlalchemy.text(
                            """DELETE FROM `combatrole_has_character` WHERE (`PartyRole_idPartyRole` = '1')
                            AND (`Character_idCharacter` = :charID)
                            AND (`RoleRange_idRoleRange` != :range)"""), {"charID": charID, "range": healerrange_id}
                        )
                    except exc.IntegrityError as e:
                        logger.warning(e)

                elif i == "DPS":
                    dpsrange_id = (lambda x: 1 if x.get("combat_role_dps") == "Melee" else 2 if x.get("combat_role_dps") == "Ranged" else None)(combat_roles)
                    logger.debug(f"DPS rangeID: {dpsrange_id}")
                    try:
                        conn.execute(sqlalchemy.text(
                            """REPLACE INTO `combatrole_has_character`
                            (`RoleRange_idRoleRange`,
                            `Character_idCharacter`,
                            `PartyRole_idPartyRole`,
                            `RoleSkill`)
                            SELECT :range, idCharacter, 3, :skill FROM `character`
                            WHERE CharacterName = :characterName"""
                        ),
                        {"range": dpsrange_id, "characterName": characterName, "skill": combat_roles["dpsSkill"]})

                        conn.execute(sqlalchemy.text(
                            """DELETE FROM `combatrole_has_character` WHERE (`PartyRole_idPartyRole` = '3')
                            AND (`Character_idCharacter` = :charID)
                            AND (`RoleRange_idRoleRange` != :range)"""), {"charID": charID, "range": dpsrange_id}
                        )
                    except exc.IntegrityError as e:
                        logger.warning(e)

                    
           #remove roles that were not selected 
            if "Tank" not in role:
                logger.info("removing tank role, not selected")
                conn.execute(sqlalchemy.text("""DELETE FROM `combatrole_has_character` WHERE (`PartyRole_idPartyRole` = '2') and (`Character_idCharacter` = :charID)"""), {"charID": charID})

            if "Healer" not in role:
                logger.info("removing healer role, not selected")
                conn.execute(sqlalchemy.text("""DELETE FROM `combatrole_has_character` WHERE (`PartyRole_idPartyRole` = '1') and (`Character_idCharacter` = :charID)"""), {"charID": charID})

            if "DPS" not in role:
                logger.info("removing DPS role, not selected")
                conn.execute(sqlalchemy.text("""DELETE FROM `combatrole_has_character` WHERE (`PartyRole_idPartyRole` = '3') and (`Character_idCharacter` = :charID)"""), {"charID": charID})

            conn.commit()

            if kwargs.get("dungeon"):
                conn.execute(sqlalchemy.text(
                    """REPLACE INTO `mythickey`
                    (`idMythicKey`, `level`, `Dungeon_id`)
                    SELECT :idmythickey, :keylevel, idDungeon FROM `dungeon`
                    WHERE DungeonName = :dungeon """),
                    {"idmythickey": Id_Mythic_Key, "keylevel": keylevel, "dungeon": dungeon}
                    )
            conn.commit()
            
    except exc.SQLAlchemyError as error:
        logger.exception(error)
        return Response(
                status=500,
                response="Unable to successfully sign up player! Please check the application logs for more details.")
    except Exception as e:
            # If something goes wrong, handle the error in this section. This might
            # involve retrying or adjusting parameters depending on the situation.
            logger.exception(e)
            return Response(
                status=500,
                response="Unable to successfully sign up player! Please check the application logs for more details.")

    return Response(status=200, response=f"Entry successful for '{playerName}'")


def get_key_info(CharacterName: str):
    with db.connect() as conn:
        MythicKey = conn.execute(sqlalchemy.text(
            """SELECT DungeonName, level FROM char_info
            WHERE CharacterName = :characterName"""
        ),
        {"characterName": CharacterName}
        ).first()
        return MythicKey

def edit_key_info(CharacterName: str, level: int, dungeon: str):
    with db.connect() as conn:
        MythicKey_ID = conn.execute(sqlalchemy.text(
            """SELECT MythicKey_id FROM `character`
            WHERE CharacterName = :characterName"""
        ),
        {"characterName": CharacterName}
        ).one_or_none()

        results = conn.execute(sqlalchemy.text(
            """UPDATE mythickey
            SET level = :level,
            Dungeon_id = (SELECT idDungeon FROM dungeon WHERE DungeonName = :dungeonName)
            WHERE idMythicKey = :mythickey_id"""
        ),
        {"level": level, "dungeonName": dungeon, "mythickey_id": MythicKey_ID}
        ).rowcount

    return results



def clear_database():
    try:
        with db.connect() as conn:
            conn.execute(sqlalchemy.text("DELETE FROM role_entries"))
            conn.execute(sqlalchemy.text("DELETE FROM characters"))
            conn.execute(sqlalchemy.text("DELETE FROM players"))

            conn.commit()
            logger.info("Database Cleared")
    except Exception as error:
        print("Error occurred - ", error)
        logger.exception(error)


def check_session_exists(groupid):
    try:
        with db.connect() as conn:
            query = conn.execute(sqlalchemy.text(f"SELECT group_ID FROM `player` WHERE group_ID = {groupid}")).fetchall()
            numFound = len(query)
            logger.debug(f"len of results: {numFound}")

            if numFound >= 1:
                logger.info("results found")
                return True
            else:
                logger.info("No results found")
                return False
    except Exception as error:
        logger.exception(error)



if __name__ == "__main__":
    # CharacterName = "Businessman"
    # with db.connect() as conn:
    #     Player_ID = conn.execute(sqlalchemy.text(
    #         """SELECT idPlayers FROM player
    #         JOIN `character` c ON c.Player_idPlayers = idPlayers
    #         WHERE CharacterName = :characterName"""),
    #         {"characterName": CharacterName}).one_or_none()
    #     if Player_ID == None:
    #         last_player = conn.execute(sqlalchemy.text(
    #             f"""SELECT Player_idPlayers FROM `character`
    #             JOIN player ON idPlayers = Player_idPlayers
    #             WHERE Player_idPlayers = 18 
    #             """
    #         )).all()
    #     else:
    #         last_player = conn.execute(sqlalchemy.text(
    #             f"""SELECT Player_idPlayers FROM `character`
    #             JOIN player ON idPlayers = Player_idPlayers
    #             WHERE Player_idPlayers = {Player_ID[0]} 
    #             """
    #         )).all()
        
    #     print(f"items found: {last_player}")
    #     print(f"length of items: {len(last_player)}")

    # r = read_current_players_db()
    # for item in r:
    #     print(item)

    players = create_dict_from_db()
    print(players)

