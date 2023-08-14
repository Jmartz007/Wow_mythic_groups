import sqlite3


def find_tables():
    try:
        conn = sqlite3.connect("Wow_mythic_groups\website\database.db")
        cursor = conn.cursor()
        print("DB Connected")
        query = "SELECT name FROM sqlite_master"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Error occurred - ", error)
    finally:
        if conn:
            conn.close()
            print("Connection closed")
    if results is None or results == [] or results == "" or len(results) == 0:
        print("No table exists")
    else:
        print(results)
        print("Tables exists")

find_tables()


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
    try:
        conn = sqlite3.connect("Wow_mythic_groups\website\database.db")
        cursor = conn.cursor()
        print("Database connected")

        query = '''SELECT p.PlayerName,
        c.CharacterName,
        c.Class, r.Role
        FROM players as p
        LEFT JOIN characters as c ON p.PlayerName = c.PlayerName
        LEFT JOIN role__entries as r ON c.CharacterName = r.CharacterName
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
    
    playerListDB = []
    for row in results:
        playerListDB.append(row)

    return playerListDB



if __name__ == "__main__":
    player_dict = add_player_dict()
    add_characters_dict(player_dict)
    print(player_dict)
    sqlPlayerDict = add_role(player_dict)
    print("\nFinal dictionary:")
    for entry in sqlPlayerDict.items():
        print(entry)
    # print(sqlPlayerDict)

    