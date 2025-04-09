#===============================================================================
#Modules being imported
#===============================================================================

import sqlite3

connection = sqlite3.connect('user_db.db')
cursor = connection.cursor()

#users table creation
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
               username TEXT PRIMARY KEY,
               password TEXT NOT NULL,
)''')

#high_scores table creation
cursor.execute('''
CREATE TABLE IF NOT EXISTS high_scores (
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               score INTEGER NOT NULL,
               FOREIGN KEY (username) REFERENCES users (username)
)''')

#sample data 
cursor.execute('''
INSERT INTO users (username, password) VALUES
('user1', 'password1')
('user2', 'password2')
('user3', 'password3')
)''')

#sample data
cursor.execute('''
INSERT INTO high_scores (username, score) VALUES
('user1', 100),
('user2', 200),
('user3', 300)
)''')

connection.commit()
connection.close()
