import sqlite3

connection  = sqlite3.connect("identifier.sqlite")
cursor = connection.cursor()

cursor.execute("SELECT * FROM events")

rows = cursor.fetchall()
print(type(rows))


new=[('rysolutions','lyon','2024.12.23')]

cursor.executemany("INSERT INTO events VALUES(?,?,?)",new)
connection.commit()



