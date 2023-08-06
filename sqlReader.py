import sqlite3


try:
    conn = sqlite3.connect("website/database.db")
    cursor = conn.cursor()
    print("DB Connected")
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='user'"
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)
    cursor.close()
except sqlite3.Error as error:
    print("Error occurred - ", error)
finally:
    if conn:
            conn.close()
            print("Connection closed")

if results == 0:
    print("No table exists")

else:
    print("Table exists")


try:

    conn = sqlite3.connect("website/database.db")
    cursor = conn.cursor()
    print("DB Connected")

    query = "SELECT * FROM user"
    cursor.execute(query)

    results = cursor.fetchall()
    print(results)

    cursor.close()

except sqlite3.Error as error:
    print("Error occurred - ", error)

finally:

        if conn:
             conn.close()
             print("Connection closed")