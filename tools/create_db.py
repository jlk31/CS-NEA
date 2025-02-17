import sqlite3

connection = sqlite3.connect('user_db.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
               username TEXT PRIMARY KEY,
               password TEXT NOT NULL,
)''')

cursor.execute('''
INSET INTO users (username, password) VALUES
('user1', 'password1')
('user2', 'password2')
('user3', 'password3')
)''')

connection.commit()
connection.close()