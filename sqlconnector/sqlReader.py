import logging
from ast import Dict, List, Try
from re import DEBUG

import sqlalchemy
from sqlalchemy import exc
from flask import Response

from logging.handlers import TimedRotatingFileHandler
from .connection_pool import init_connection_pool

logger = logging.getLogger(f"main.{__name__}")

db = init_connection_pool()

def create_dict_from_db(groupid) -> dict:

    # Retrieves players from the DB and adds them to a dictionary
    player_dict = {}

    try:
        with db.connect() as conn:
            # Execute the query and fetch all results
            player_entries = conn.execute(
                sqlalchemy.text( f"SELECT * FROM players WHERE group_id = '{groupid}'" )
            ).fetchall()

            charEntries = conn.execute(
                sqlalchemy.text( f'''SELECT p.PlayerName, c.CharacterName, c.Class
            FROM players as p LEFT JOIN characters as c ON p.PlayerName = c.PlayerName AND p.group_id = c.group_id WHERE p.group_id = {groupid}
                                ''' )
            ).fetchall()
            logger.debug(charEntries)
            logger.info("Query from tables (players, characters) executed successfully")

            roleEntries = conn.execute(
                sqlalchemy.text( f'''SELECT c.CharacterName, r.Role, c.Class, r.TankConfidence, r.HealerConfidence FROM characters as c
        LEFT JOIN role_entries as r
        ON r.CharacterName = c.CharacterName AND r.group_id = c.group_id WHERE c.group_id = {groupid}
                                ''' )
            ).fetchall()

            logger.info("Query from tables (characters, role_entries) executed successfully")

            #add results to dictionary and create a value of type dict as the entry for that key
            
        # for i in player_entries:
        #     print(i[1])
        # for row in player_entries:
        #     print(row[1])

        for row in player_entries:
            player_dict[row[1]] = {}

    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
    except Exception as error:
        logger.exception(error)
  
       
    # add characters to the player entries
    try:
        for row in charEntries:
            # print(f"\nnew row: {row}:")
            for key, value in player_dict.items():
                # print(f"key is {key}")
                # print(f"Value is: {value}")
                # print(f"row is {row}, and row[0] is {row[0]}, row[2] is: {row[2]}")
                if key == row[0] and (len(value)==0):
                    # print("Row matches key")
                    # print(value)
                    # print(f"key {key} is empty")
                    player_dict[row[0]] = {row[1] : {"Class": row[2]  }}   # <--- where to add a characters information to the dictionary (Character : {Class: Priest, Key: 14, etc}) from sql query
                    # print(f"Added {row}")
                    # print(player_dict)
                    # print("")
                elif key == row[0]:
                    # print(f"key {key} has value of {value} already.")
                    # print(f"ADDING key: {key}, Value: {row[1]}, {row[2]}")
                    player_dict[row[0]].update({row[1]: {"Class": row[2]} })  # <----------- here too
                    # print(player_dict)
                    # print("")
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
            # print(i)
            # creating a new list to add multiple roles if needed

            newList = []
            if i[0] in newDict.keys():
                # print(f'''If loop: {newDict[i[0]]["Role"]}''')
                # print(f'''newdict: {newDict[i[0]]["Role"][0]}''')
                if len(newDict[i[0]]["Role"])>=2:
                    # print(i[1])
                    newList.extend([newDict[i[0]]["Role"][0], newDict[i[0]]["Role"][1], i[1]])
                    # print(newList)
                    newDict.update({i[0]: {"Role": newList, "Tconf": i[3], "Hconf": i[4]  }})
                    continue
                newList.extend([newDict[i[0]]["Role"][0], i[1]])
                # print(f"new list: {newList}")
                # print(f"newlist extend {newDict[i[0]][0]}, { i[1]}")
                newDict.update({i[0]: {"Role": newList, "Tconf": i[3], "Hconf": i[4]  }})
                # print(newDict)
            else:
                newList.append(i[1])
                # print(f"Else loop: {i[1]}")
                # print(f"newList: {newList}")
                newDict.update({i[0]:{"Role": newList, "Tconf": i[3], "Hconf": i[4] }})
                # print(newDict)
        # print(newDict)
        for key, value in newDict.items():
            for k, v in player_dict.items():
                if key in v:
                    player_dict[k][key].update( value)

        logger.debug(player_dict)
        logger.info("sqlReader successfully created dictionary from database")
        

    except Exception as error:
        logger.error(error)

    return player_dict    



def read_current_players_db() -> List:
    playerListDB = []
    db = init_connection_pool()
    try:
       
        with db.connect() as conn:
            # Execute the query and fetch all results
            # results = conn.execute( sqlalchemy.text('''SELECT p.PlayerName, c.CharacterName, c.ClassName, r.Role
            #      FROM player as p LEFT JOIN character as c ON p.PlayerName = c.PlayerName
            #                                         LEFT JOIN role_entries as r ON c.CharacterName = r.CharacterName
            #     '''
            #     )).fetchall()
            results = conn.execute(sqlalchemy.text("SELECT * FROM full_char_info")).fetchall()
            
        for row in results:
            playerListDB.append(row)

    except Exception as e:
        logger.exception(e)
        return Response(
            status=500,
            response="Unable to read the players from the DB")
    logger.info("Successfully read the players from the database")
    return playerListDB
    
def print_player_dict(sqlPlayerDict: Dict):
    logger.debug("\nFinal dictionary:")
    for entry in sqlPlayerDict.items():
        logger.debug(entry)
    return sqlPlayerDict

def delete_query(CharacterName):
    db = init_connection_pool()
    try:
        with db.connect() as conn:
            query = conn.execute(sqlalchemy.text(f'''
                                                 SELECT c.CharacterName, c.Class, r.Role FROM characters as c LEFT JOIN role_entries as r on c.CharacterName = r.CharacterName WHERE c.CharacterName LIKE "{CharacterName}"
                                                 ''')).first()
            return query

    except exc.StatementError as sqlstatementerr:
        logger.exception(sqlstatementerr)
    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
        return Response(status=400, response=f"SQL Error: {sqlerror}")
    except Exception as e:
        logger.exception(e)
        return Response(status=500, response="Error deleting player")

def delete_entry(CharacterName, groupid):
    db = init_connection_pool()
    try:
        with db.connect() as conn:
            query = sqlalchemy.text(f'''
                                    SELECT CharacterName FROM characters WHERE CharacterName =
                                    "{CharacterName}" AND group_id = "{groupid}"
                                    ''')
            conn.execute(query)

            LastCharacterQuery = sqlalchemy.text(f'''
                                            SELECT PlayerName, min(CharacterName) FROM characters WHERE group_id = {groupid}
                                            group by PlayerName
                                            having COUNT(*) = 1 and min(CharacterName) = "{CharacterName}"
                                            ''')
            CursorLastCharacter = conn.execute(LastCharacterQuery).one_or_none()

            if CursorLastCharacter is not None:
                PlayerName = CursorLastCharacter[0]
                delete = conn.execute(sqlalchemy.text(f'''
                                                 DELETE FROM players WHERE PlayerName =
                                                  "{PlayerName}" AND group_id = "{groupid}"
                                                 '''))

                conn.commit()
                logger.info(f"Deleted: {str(delete.rowcount)} Character and  {PlayerName}")
                return "Deleted: " + str(delete.rowcount) + " Character and " + PlayerName

            else:
                result = conn.execute(sqlalchemy.text(f'''
                                                 DELETE FROM characters WHERE CharacterName =
                                                  "{CharacterName}" and group_id = "{groupid}"
                                                 '''))
                conn.commit()
                logger.info(f"{result.rowcount}  rows matched for deletion")
                logger.info(f"Deleted {query}")
                return "Deleted: " + str(result.rowcount)


    except exc.StatementError as sqlstatementerr:
        logger.exception(sqlstatementerr)
    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
        return Response(status=400, response=f"SQL Error: {sqlerror}")
    except Exception as e:
        logger.exception(e)
        return Response(status=500, response="Error deleting player")



def player_entry(playerName: str, characterName: str, className: str, role: list[str], combat_role: list[str], **kwargs):

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
            stmt = sqlalchemy.text("SELECT idCharacter, CharacterName FROM `character` WHERE CharacterName = :charName")
            result = conn.execute(stmt, {"charName": characterName}).first()
            if result:
                logger.info(f"character {characterName} already exists")
            elif not result:
                logger.info(f"adding character {characterName}")
                insert_stmt = sqlalchemy.text(
                    """INSERT INTO `mythicsdb`.`character`
                    (`CharacterName`, `ClassName`, `PlayerRating`, `MythicKey_id`,`Player_idPlayers`)
                    VALUES
                    (:characterName, :className, 'Intermediate', 1, :playerID)""")
            
                conn.execute(insert_stmt, {"characterName": characterName, "className": className, "playerID": playerID})
                result = conn.execute(stmt, {"charName": characterName}).first()
                logger.debug(result)

            charID = result[0]

            for i in role:
                # for key, value in kwargs.items():
                # conn.execute(sqlalchemy.text("""UPDATE `mythicsdb`.`partyrole_has_character`, `partyrole`, `character`
                #                             SET 
                #                             `PartyRole_idPartyRole` = `partyrole`.`idPartyRole`,
                #                             `Character_idCharacter` = `character`.`idCharacter`
                #                             WHERE 
                #                             `partyrole`.`PartyRoleName` = :role AND
                #                             `character`.`CharacterName` = :charName"""),
                #                             {"charName": characterName, "role": i})
                if  i == "Tank":
                    try:
                        conn.execute(sqlalchemy.text(
                            """INSERT INTO `mythicsdb`.`partyrole_has_character`
                            (`PartyRole_idPartyRole`,
                            `Character_idCharacter`)
                            SELECT 2, idCharacter FROM `character`
                            WHERE CharacterName = :characterName"""),
                            {"characterName": characterName})
                        logger.debug(f"added {characterName} with role {i} ")
                    except exc.IntegrityError as e:
                        logger.warning(e)

                elif i == "Healer":
                    try:
                        conn.execute(sqlalchemy.text(
                            """INSERT INTO `mythicsdb`.`partyrole_has_character`
                            (`PartyRole_idPartyRole`,
                            `Character_idCharacter`)
                            SELECT 1, idCharacter FROM `character`
                            WHERE CharacterName = :characterName"""),
                            {"characterName": characterName})
                        logger.debug(f"added {characterName} with role {i} ")
                    except exc.IntegrityError as e:
                        logger.warning(e)                    

                elif i == "DPS":
                    try:
                        conn.execute(sqlalchemy.text(
                            """INSERT INTO `mythicsdb`.`partyrole_has_character`
                            (`PartyRole_idPartyRole`,
                            `Character_idCharacter`)
                            SELECT 3, idCharacter FROM `character`
                            WHERE CharacterName = :characterName"""),
                            {"characterName": characterName})
                        logger.debug(f"added {characterName} with role {i} ")
                    except exc.IntegrityError as e:
                        logger.warning(e)
           #remove roles that were not selected 
            if "Tank" not in role:
                logger.info("removing tank role, not selected")
                conn.execute(sqlalchemy.text("""DELETE FROM `mythicsdb`.`partyrole_has_character` WHERE (`PartyRole_idPartyRole` = '2') and (`Character_idCharacter` = :charID)"""), {"charID": charID})
            if "Healer" not in role:
                logger.info("removing healer role, not selected")
                conn.execute(sqlalchemy.text("""DELETE FROM `mythicsdb`.`partyrole_has_character` WHERE (`PartyRole_idPartyRole` = '1') and (`Character_idCharacter` = :charID)"""), {"charID": charID})
            if "DPS" not in role:
                logger.info("removing DPS role, not selected")
                conn.execute(sqlalchemy.text("""DELETE FROM `mythicsdb`.`partyrole_has_character` WHERE (`PartyRole_idPartyRole` = '3') and (`Character_idCharacter` = :charID)"""), {"charID": charID})
            # conn.commit()

            # update combat role

            for j in combat_role:
                if  j == "Melee":
                    try:                        
                        conn.execute(sqlalchemy.text(
                            """INSERT INTO `mythicsdb`.`combatrole_has_character`
                            (`CombatRole_idCombatRole`,
                            `Character_idCharacter`)
                            SELECT 1, idCharacter FROM `character`
                            WHERE CharacterName = :characterName
                            """),
                            {"characterName": characterName})
                        logger.debug(f"added {characterName} with combat_role {i} ")
                    except exc.IntegrityError as e:
                        logger.warning(e)
                    
                if  j == "Ranged":
                    try:                        
                        conn.execute(sqlalchemy.text(
                            """INSERT INTO `mythicsdb`.`combatrole_has_character`
                            (`CombatRole_idCombatRole`,
                            `Character_idCharacter`)
                            SELECT 2, idCharacter FROM `character`
                            WHERE CharacterName = :characterName
                            """),
                            {"characterName": characterName})
                        logger.debug(f"added {characterName} with combat_role {i} ")
                    except exc.IntegrityError as e:
                        logger.warning(e)

            if "Melee" not in combat_role:
                logger.info("removing melee role, not selected")
                conn.execute(sqlalchemy.text("""DELETE FROM `mythicsdb`.`combatrole_has_character` WHERE (`CombatRole_idCombatRole` = '1') and (`Character_idCharacter` = :charID)"""), {"charID": charID})
            if "Ranged" not in combat_role:
                logger.info("removing ranged role, not selected")
                conn.execute(sqlalchemy.text("""DELETE FROM `mythicsdb`.`combatrole_has_character` WHERE (`CombatRole_idCombatRole` = '2') and (`Character_idCharacter` = :charID)"""), {"charID": charID})

            conn.commit()
    except exc.SQLAlchemyError as error:
        logger.exception(error)
        return Response(
                status=500,
                response="Unable to successfully sign up player! Please check the application logs for more details.")
    except Exception as e:
            # If something goes wrong, handle the error in this section. This might
            # involve retrying or adjusting parameters depending on the situation.
            # [START_EXCLUDE]
            logger.exception(e)
            return Response(
                status=500,
                response="Unable to successfully sign up player! Please check the application logs for more details.")
        # [END_EXCLUDE]
    # [END cloud_sql_mysql_sqlalchemy_connection]

    return Response(status=200, response=f"Entry successful for '{playerName}'")


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
    # sqlPlayerDict = create_dict_from_db()
    # print_player_dict(sqlPlayerDict)

    r = read_current_players_db()
    for item in r:
        print(item)