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
               _id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               score INTEGER NOT NULL,
               FOREIGN KEY (username) REFERENCES users (username)
)''')

#create games table
cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
               game_id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               score INTEGER NOT NULL,
               date_played TEXT NOT NULL,
               duration INTEGER NOT NULL,
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

#sample data
cursor.execute('''
INSERT INTO games (username, score, date_played, duration) VALUES
('user1', 100, '2023-10-01', 30),
('user2', 200, '2023-10-02', 45),
('user3', 300, '2023-10-03', 60)
)''')

#commit the changes and close the connection
connection.commit()
connection.close()
