import sqlite3

#create a table for usernames

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE
    )'
''')

#create a table for passwords

c.execute(''''
    CREATE TABLE IF NOT EXISTS passwords (
    user_id INTEGER PRIMARY KEY,
    password TEXT NOT NULL
    )'
''')

#create a table for userIDs


