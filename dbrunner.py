import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

cursor.execute("DROP TABLE services_service1page;")


# Commit the changes and close the connection
conn.commit()
conn.close()
