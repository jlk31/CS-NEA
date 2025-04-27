import tkinter as tk
from tkinter import messagebox
import sqlite3
from database.db_manager import DBManager

class RevisionMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Revision Menu")

#================================================================
#question entry
#================================================================

        self.question_label = tk.Label(root, text="Enter your question:")
        self.question_label.pack(pady=5)

        self.question_entry = tk.Entry(root, width=50)
        self.question_entry.pack(pady=5)

#================================================================
#save question button
#================================================================

        self.save_button = tk.Button(root, text="Save Question", command=self.save_question)
        self.save_button.pack(pady=10)

#================================================================
#answer entry
#================================================================

        self.answer_label = tk.Label(root, text="Enter your answer:")
        self.answer_entry = tk.Entry(root, width=50)

#================================================================
#save question
#================================================================

    def save_question(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Warning", "Please enter a question before saving.")
            return

        try:
            db_manager = DBManager("database/user_db.db")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while connecting to the database: {e}")
            return

        # Save the question to the database
        db_manager.save_question(question)
        print(f"Question saved: {question}")

#================================================================
#reset question entry and show answer entry
#================================================================

        self.question_entry.delete(0, tk.END)
        self.question_label.pack_forget()
        self.question_entry.pack_forget()
        self.save_button.pack_forget()

        self.answer_label.pack(pady=5)
        self.answer_entry.pack(pady=5)

#================================================================
#save answer button
#================================================================

        self.save_answer_button = tk.Button(self.root, text="Save Answer", command=self.save_answer)
        self.save_answer_button.pack(pady=10)

    def save_answer(self):
        answer = self.answer_entry.get().strip()
        if not answer:
            messagebox.showwarning("Warning", "Please enter an answer before saving.")
            return

#================================================================
#save answer
#================================================================

        print(f"Answer saved: {answer}")

#================================================================
#reset answer entry and return to question entry
#================================================================

        self.answer_entry.delete(0, tk.END)
        self.answer_label.pack_forget()
        self.answer_entry.pack_forget()
        self.save_answer_button.pack_forget()

        self.question_label.pack(pady=5)
        self.question_entry.pack(pady=5)
        self.save_button.pack(pady=10)
