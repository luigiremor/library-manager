import tkinter as tk
from tkinter import messagebox

from database.database_manager import DatabaseManager


class LibraryController:
    def __init__(self, db_name):
        self.db = DatabaseManager(db_name)

    def create_librarian(self, name, email, password):
        created = self.db.create_librarian(name, email, password)
        if created:
            messagebox.showinfo("Success", "Librarian created successfully")
        else:
            messagebox.showerror("Error", "Failed to create librarian")

    def create_student(self, name, email, cpf, tel, registration):
        self.db.create_student(name, email, cpf, tel, registration)
        messagebox.showinfo("Success", "Student created successfully")

    def get_all_students(self):
        return self.db.get_all_students()

    def create_book_item(self, title, author, release_year):
        last_inserted_id = self.db.create_book_item(title, author, release_year)
        messagebox.showinfo("Success", f"Book item created successfully with id {last_inserted_id}")

    def get_all_items(self):
        return self.db.get_all_items()

    def get_all_items_by_type(self, item_type):
        return self.db.get_all_items_by_type(item_type)

    def update_book_item(self, item_id, title, author, release_year):
        self.db.update_book_item(item_id, title, author, release_year)
        messagebox.showinfo("Success", f"Book item with id {item_id} updated successfully")

    def delete_item(self, item_id):
        self.db.delete_item(item_id)
        messagebox.showinfo("Success", f"Item with id {item_id} deleted successfully")

    def reserve_item(self, item_id, student_id):
        self.db.reserve_item(item_id, student_id)
        messagebox.showinfo("Success", f"Item with id {item_id} reserved by student with id {student_id}")

    def lend_item(self, item_id, student_id):
        self.db.lend_item(item_id, student_id)
        messagebox.showinfo("Success", f"Item with id {item_id} lent to student with id {student_id}")

    def cancel_item_reservation(self, item_id):
        self.db.cancel_item_reservation(item_id)
        messagebox.showinfo("Success", f"Reservation for item with id {item_id} cancelled")

    def return_item(self, item_id):
        self.db.return_item(item_id)
        messagebox.showinfo("Success", f"Item with id {item_id} returned successfully")

    def close_connection(self):
        self.db.close_connection()
