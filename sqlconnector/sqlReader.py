import sqlalchemy
from sqlalchemy import exc
from flask import Response
import logging
from logging.handlers import TimedRotatingFileHandler
from website import init_connection_pool

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', handlers=[logging.FileHandler("var/log/myapp.log"), stream_handler])


def create_dict_from_db() -> dict:
    db = init_connection_pool()
    # Retrieves players from the DB and adds them to a dictionary
    player_dict = {}

    try:
        with db.connect() as conn:
            # Execute the query and fetch all results
            player_entries = conn.execute(
                sqlalchemy.text( "SELECT * FROM players" )
            ).fetchall()
            #add results to dictionary and create a value of type dict as the entry for that key
            
        for i in player_entries:
            print(i[0])
        for row in player_entries:
            print(row[1])

        for row in player_entries:
            player_dict[row[1]] = {}
      
    except Exception as error:
        logger.exception(error)
  
       
    # add characters to the player entries
    try:
        with db.connect() as conn:
            # Execute the query and fetch all results
            results = conn.execute(
                sqlalchemy.text( '''SELECT p.PlayerName, c.CharacterName, c.Class
            FROM players as p LEFT JOIN characters as c ON p.PlayerName = c.PlayerName
                                ''' )
            ).fetchall()
            logger.debug(results)
            logger.info("Query from tables (players, characters) executed successfully")

        for row in results:
            print(f"\nnew row: {row}:")
            for key, value in player_dict.items():
                print(f"key is {key}")
                print(f"Value is: {value}")
                print(f"row is {row}, and row[0] is {row[0]}, row[2] is: {row[2]}")
                if key == row[0] and (len(value)==0):
                    print("Row matches key")
                    print(value)
                    print(f"key {key} is empty")
                    player_dict[row[0]] = {row[1] : {"Class": row[2]}}  # <--- where to add a characters information to the dictionary (Character : {Class: Priest, Key: 14, etc}) from sql query
                    print(f"Added {row[1]}")
                    print(player_dict)
                    print("")
                elif key == row[0]:
                    print(f"key {key} has value of {value} already.")
                    print(f"ADDING key: {key}, Value: {row[1]}, {row[2]}")
                    player_dict[row[0]].update({row[1]: {"Class": row[2]}})
                    print(player_dict)
                    print("")
                else:
                    print("row did not match key\n")

        logger.info("Characters added to players dictionary")

    except exc.SQLAlchemyError as sqlerror:
        logger.exception(sqlerror)
    except Exception as error:
        logger.exception(error)
        
    
    # add role information to the characters in the dictionary
    try:
        with db.connect() as conn:
            # Execute the query and fetch all results
            results = conn.execute(
                sqlalchemy.text( '''SELECT c.CharacterName, r.Role, c.Class FROM characters as c
        LEFT JOIN role_entries as r
        ON r.CharacterName = c.CharacterName
                                ''' )
            ).fetchall()

            logger.info("Query from tables (characters, role_entries) executed successfully")

        newDict = {}
        for i in results:
            # creating a new list to add multiple roles if needed
            newList = []
            if i[0] in newDict.keys():
                newList.extend([newDict[i[0]][0], i[1]])
                newDict.update({i[0]: newList })
            else:
                newList.append(i[1])
                newDict.update({i[0]: newList})

        for key, value in newDict.items():
            for k, v in player_dict.items():
                if key in v:
                    player_dict[k][key].update({"Role" : value})

        successMsg = "\n------------ sqlReader successfully created dictionary from database ------------"
        logger.debug(player_dict)
        logger.info(successMsg)
        

    except Exception as error:
        logger.error(error)

    return player_dict    



def read_current_players_db():
    playerListDB = []
    db = init_connection_pool()
    try:
       
        with db.connect() as conn:
            # Execute the query and fetch all results
            results = conn.execute( sqlalchemy.text('''SELECT p.PlayerName, c.CharacterName, c.Class, r.Role
                 FROM players as p LEFT JOIN characters as c ON p.PlayerName = c.PlayerName
                                                    LEFT JOIN role_entries as r ON c.CharacterName = r.CharacterName
                '''
                )).fetchall()
            
        # Convert the results into a list of dicts representing votes
        for row in results:
            playerListDB.append(row)

    except Exception as e:
        # If something goes wrong, handle the error in this section. This might
        # involve retrying or adjusting parameters depending on the situation.
        # [START_EXCLUDE]
        logger.exception(e)
        return Response(
            status=500,
            response="Unable to read the players from the DB"
    )
        # [END_EXCLUDE]
    # [END cloud_sql_mysql_sqlalchemy_connection]
    logger.info("Successfully read the players from the database")
    return playerListDB
    
def print_player_dict(sqlPlayerDict):
    print("\nFinal dictionary:")
    for entry in sqlPlayerDict.items():
        print(entry)
    return sqlPlayerDict


if __name__ == "__main__":
    sqlPlayerDict = create_dict_from_db()
    print_player_dict(sqlPlayerDict)

    