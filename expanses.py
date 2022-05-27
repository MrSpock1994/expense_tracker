import sqlite3

# Creating the Expanses DataBase
conn = sqlite3.connect("Expenses.db")
# creating a cursor
cursor = conn.cursor()
# create table
cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
    name text,
    price real,
    date text,
    description text)
    """)

conn.commit()
conn.close()