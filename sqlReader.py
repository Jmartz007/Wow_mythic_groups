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
        print(f"new row: {row}:\n")
        for key, value in player_dict.items():
            print(f"key is {key}")
            print(f"Value is: {value}")
            print(f"row is {row}, and row[0] is {row[0]}")
            if key == row[0] and (len(value)==0):
                print("Row matches key")
                print(value)
                print(f"key {key} is empty")
                player_dict[row[0]] = {row[1] : ""}
                print(f"Added {row[1]}")
                print(player_dict)
                print("")
            elif key == row[0]:
                print(f"key {key} has value of {value} already.")
                print(f"ADDING key: {key}, Value: {row[1]}")
                player_dict[row[0]].update({row[1]: ""})
                print(player_dict)
                print("")
            else:
                print("row did not match key\n")
                
                
    
    print(player_dict)

player_dict = add_player_dict()
add_characters_dict(player_dict)

def add_role():
    try:
        conn = sqlite3.connect("Wow_mythic_groups\website\database.db")
        cursor = conn.cursor()
        print("DB Connected")

        query = '''SELECT c.CharacterName, r.Role FROM characters as c
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

    return results


results = add_role()
newDict = {}
pList = []
for i in results:
    print(i)
    if i[0] not in pList:
        pList.append(i[0])
        newDict[i[0]] = {i[1]}

print(pList)
print(newDict)

rList = []
for i in results:
    # print(i[1])
    for key, value in newDict.items():
        if i[0] == key:
            print(key, i[1])

# %%
import pandas as pd

df = pd.read_csv(r"c:\Users\jeffi\Documents\Coding Projects\WoW Mythic Group Maker\sample.csv")
print(df)


# %%
df.drop(columns=["Unnamed: 0"], inplace=True)
df
# %%
df = df.groupby(["0", "1"]).count()
df.to_dict()

# %%
