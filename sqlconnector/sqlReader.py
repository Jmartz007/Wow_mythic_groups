import sqlalchemy
from flask import Response
import datetime
import logging
import sqlite3
from website import init_connection_pool

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', handlers=[logging.FileHandler("myapp.log"), stream_handler])


db = init_connection_pool()

# get_index_context gets data required for rendering HTML application
def add_player_dict(db: sqlalchemy.engine.base.Engine) -> dict:
    """Retrieves players from the DB and adds them to a dictionary"""
    player_dict = {}

    with db.connect() as conn:
        # Execute the query and fetch all results
        player_entries = conn.execute(
            sqlalchemy.text( "SELECT * FROM players" )
        ).fetchall()
        
        for i in conn.column_descriptions:
            print(i[0])
            for row in player_entries:
                   print(row[1])


        for row in player_entries:
            player_dict[row[1]] = {}
       
    return  player_dict



def add_player_dict():
    try:
        conn = sqlite3.connect("Wow_mythic_groups\website\database.db")
        cursor = conn.cursor()
        print("DB Connected")

        query = "SELECT * FROM players"
        cursor.execute(query)

        results = cursor.fetchall()


        cursor.close()

    except sqlite3.Error as error:
        print("Error occurred - ", error)

    finally:
        if conn:
            conn.close()
            print("Connection closed")


    for i in cursor.description:
        print(i[0])
    for row in results:
        print(row[1])


    player_dict = {}

    for row in results:
        player_dict[row[1]] = {}

    print(player_dict)
    return(player_dict)


def add_characters_dict(player_dict):
    try:
        conn = sqlite3.connect("Wow_mythic_groups\website\database.db")
        cursor = conn.cursor()
        print("Database connected")

        query = '''SELECT p.PlayerName,
        c.CharacterName,
        c.Class
        FROM players as p
        LEFT JOIN characters as c ON p.PlayerName = c.PlayerName
        '''

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error occurred - ", error)

    finally:
        if conn:
            conn.close()
            print("Connection closed")

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
                
    print(player_dict)


def add_role(player_dict):
    try:
        conn = sqlite3.connect("Wow_mythic_groups\website\database.db")
        cursor = conn.cursor()
        print("DB Connected")

        query = '''SELECT c.CharacterName, r.Role, c.Class FROM characters as c
        LEFT JOIN role__entries as r
        ON r.CharacterName = c.CharacterName'''
        cursor.execute(query)

        results = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error occurred - ", error)

    finally:
        if conn:
            conn.close()
            print("Connection closed")

    # print(f"Results: {results}")
    newDict = {}
    for i in results:
        newList = []
        if i[0] in newDict.keys():
            newList.extend([newDict[i[0]][0], i[1]])
            newDict.update({i[0]: newList })
        else:
            newList.append(i[1])
            newDict.update({i[0]: newList})
    
    # print(newDict)
    # print("New DICT ^^^^")
    # print(newDict)
    for key, value in newDict.items():
        for k, v in player_dict.items():
            if key in v:
                player_dict[k][key].update({"Role" : value})

    print(f"\n------------ sqlReader successfully created dictionary from database ------------")
    return player_dict


def create_dict():
    player_dict = add_player_dict()
    add_characters_dict(player_dict)
    print(player_dict)
    sqlPlayerDict = add_role(player_dict)
    print("\nFinal dictionary:")
    for entry in sqlPlayerDict.items():
        print(entry)
    return sqlPlayerDict

def read_current_players_db():
    playerListDB = []
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
            response="Unable to successfully sign up player! Please check the "
            "application logs for more details.",
    )
        # [END_EXCLUDE]
    # [END cloud_sql_mysql_sqlalchemy_connection]

    return playerListDB
    

# save_vote saves a vote to the database that was retrieved from form data
def save_vote(db: sqlalchemy.engine.base.Engine, team: str) -> Response:
    """Saves a single vote into the database.

    Args:
        db: Connection to the database.
        team: The identifier of a team the vote is casted on.

    Returns:
        A HTTP response that can be sent to the client.
    """
    time_cast = datetime.datetime.now(tz=datetime.timezone.utc)
    # Verify that the team is one of the allowed options
    if team != "TABS" and team != "SPACES":
        logger.warning(f"Received invalid 'team' property: '{team}'")
        return Response(
            response="Invalid team specified. Should be one of 'TABS' or 'SPACES'",
            status=400,
        )

    # [START cloud_sql_mysql_sqlalchemy_connection]
    # Preparing a statement before hand can help protect against injections.
    stmt = sqlalchemy.text(
        "INSERT INTO votes (time_cast, candidate) VALUES (:time_cast, :candidate)"
    )
    try:
        # Using a with statement ensures that the connection is always released
        # back into the pool at the end of statement (even if an error occurs)
        with db.connect() as conn:
            conn.execute(stmt, parameters={"time_cast": time_cast, "candidate": team})
            conn.commit()
    except Exception as e:
        # If something goes wrong, handle the error in this section. This might
        # involve retrying or adjusting parameters depending on the situation.
        # [START_EXCLUDE]
        logger.exception(e)
        return Response(
            status=500,
            response="Unable to successfully cast vote! Please check the "
            "application logs for more details.",
        )
        # [END_EXCLUDE]
    # [END cloud_sql_mysql_sqlalchemy_connection]

    return Response(
        status=200,
        response=f"Vote successfully cast for '{team}' at time {time_cast}!",
    )




if __name__ == "__main__":
    player_dict = add_player_dict()
    add_characters_dict(player_dict)
    print(player_dict)
    sqlPlayerDict = add_role(player_dict)
    print("\nFinal dictionary:")
    for entry in sqlPlayerDict.items():
        print(entry)
    # print(sqlPlayerDict)

    