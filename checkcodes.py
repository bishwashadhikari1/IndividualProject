import sqlite3

user_info = sqlite3.connect("databases/123.db")
c = user_info.cursor()
c.execute("SELECT * FROM user_records")
d = c.fetchall()
print(d)


