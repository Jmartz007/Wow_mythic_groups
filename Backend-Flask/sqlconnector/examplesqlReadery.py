import connect_localconnection
# from connection_pool import init_connection_pool
import logging
import sqlalchemy
from sqlalchemy import exc
import os

logger = logging.getLogger(f"main.{__name__}")

def init_connection_pool() -> sqlalchemy.engine.base.Engine:    
    if os.environ.get('LOCAL_CONNECTION_IP'):
        return connect_localconnection.local_conn()

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )

db = init_connection_pool()

def create_dict_from_db() -> dict:

    # Retrieves players from the DB and adds them to a dictionary
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
            print(i)
            
            # creating a new list to add multiple roles if needed
            newList = []
            if i[0] in newDict.keys():
                print(f'''If loop: {newDict[i[0]]["Role"]}''')
                print(f'''newdict: {newDict[i[0]]["Role"][0]}''')
                if len(newDict[i[0]]["Role"])>=2:
                    # print(i[1])
                    newList.extend([newDict[i[0]]["Role"][0], newDict[i[0]]["Role"][1], i[1]])
                    # print(newList)

                    if i[1] == "Tank":
                        newDict[i[0]].update({"Role": newList, "Tank Skill": i[3]})
                    elif i[1] == "Healer":
                        newDict[i[0]].update({"Role": newList, "Healer Skill": i[3]})
                    elif i[1] == "DPS":
                        newDict[i[0]].update({"Role": newList, "DPS Skill": i[3]})
                    continue
                newList.extend([newDict[i[0]]["Role"][0], i[1]])
                # print(f"new list: {newList}")
                # print(f"newlist extend {newDict[i[0]][0]}, { i[1]}")
                if i[1] == "Tank":
                    newDict[i[0]].update({"Role": newList, "Tank Skill": i[3]})
                elif i[1] == "Healer":
                    newDict[i[0]].update({"Role": newList, "Healer Skill": i[3]})
                elif i[1] == "DPS":
                    newDict[i[0]].update({"Role": newList, "DPS Skill": i[3]})
                # print(newDict)
            else:
                newList.append(i[1])
                print(f"Else loop: {i[1]}")
                print(f"newList: {newList}")
                if i[1] == "Tank":
                    newDict.update({i[0]:{"Role": newList, "Tank Skill": i[3]}})
                elif i[1] == "Healer":
                    newDict.update({i[0]:{"Role": newList, "Healer Skill": i[3]}})
                elif i[1] == "DPS":
                    newDict.update({i[0]:{"Role": newList, "DPS Skill": i[3]}})
                print(newDict)
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

if __name__=="__main__":
    player_dict = create_dict_from_db()
    print("----------------")
    print(player_dict)