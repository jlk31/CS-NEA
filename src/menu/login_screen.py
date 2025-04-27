#===============================================================================
#Modules being imported
#===============================================================================

import sqlite3
import tkinter as tk
from tkinter import messagebox
import hashlib
from src.menu.login_screen import LoginScreen

#===============================================================================
#login screen class
#===============================================================================

class LoginScreen:
    
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title('Login Screen')

        tk.Label(self.login_window, text = 'Username').pack()
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack()

        tk.Label(self.login_window, text = 'Password').pack()
        self.password_entry = tk.Entry(self.login_window, show = '*')
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_window, text = 'Login', command = self.login)
        self.login_button.pack()

        self.login_window.mainloop()

    def login(self):
        connection = sqlite3.connect('user_db.db')
        cursor = connection.cursor()

        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            self.show_profile(user)
        else:
            messagebox.showerror('Error', 'Invalid username or password')

        connection.close()

    def show_profile(self, user):
        self.login_window.destroy()
        self.profile_window = tk.Tk()
        self.profile_window.title(f' Profile of {user[0]}')

        tk.Label(self.profile_window, text = f' Username: {user[0]}').pack()

        self.profile_window.mainloop()

if __name__ == '__main__':
    LoginScreen()