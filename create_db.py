#python3 create_db.py
# sqlite3 db.sqlite "SELECT * FROM people"

import sqlite3
from datetime import datetime, date

conn = sqlite3.connect("db.sqlite",detect_types=sqlite3.PARSE_DECLTYPES) 
conn.execute("DROP TABLE IF EXISTS calendar")
conn.execute("DROP TABLE IF EXISTS people")

#people
conn.execute("CREATE TABLE people (\
 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
 firstname TEXT NOT NULL,\
 lastname TEXT NOT NULL,\
 phone_number TEXT NULL,\
 note TEXT NULL)")
conn.execute("INSERT INTO people(firstname, lastname, phone_number) values(?, ?, ?)", ("Adam","Smith", "555-01-01"))
conn.execute("INSERT INTO people(firstname, lastname, note) values(?, ?, ?)", ("Bob","B.", "black list"))
conn.commit()

print("Table people")
cur = conn.cursor()
cur.execute("SELECT * FROM people")
for row in cur:
  print(row)
print("")
  
conn.close()