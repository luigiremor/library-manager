import tkinter as tk
from tkinter import messagebox

from database.database_manager import DatabaseManager


class LibraryController:
    def __init__(self, db_name):
        self.db = DatabaseManager(db_name)

    def login(self, email, password):
        is_logged_in = self.db.login(email, password)
        if is_logged_in:
            return True
        else:
            messagebox.showerror("Error", "Invalid email or password")
            return False

    def create_librarian(self, name, email, password):
        is_created = self.db.create_librarian(name, email, password)

        if is_created:
            messagebox.showinfo("Success", "Librarian created successfully")
        else:
            messagebox.showerror(
                "Error", "Librarian with this email already exists")

        return is_created

    def create_student(self, name, email, cpf, tel, registration):
        is_created = self.db.create_student(
            name, email, cpf, tel, registration)
        if is_created:
            messagebox.showinfo("Success", "Student created successfully")
        else:
            messagebox.showerror(
                "Error", "Student with this registration already exists")

    def delete_student_by_registration(self, registration):
        self.db.delete_student_by_registration(registration)

    def get_all_students(self):
        return self.db.get_all_students()

    def get_student_by_registration(self, registration):
        return self.db.get_student_by_registration(registration)

    def create_book_item(self, title, release_year, author):
        last_inserted_id = self.db.create_book_item(
            title, release_year, author)
        messagebox.showinfo(
            "Success", f"Book item created successfully with id {last_inserted_id}")

    def create_article_item(self, title, release_year, abstract, word_count, author, language, keywords):
        last_inserted_id = self.db.create_article_item(
            title, release_year, abstract, word_count, author, language, keywords)
        messagebox.showinfo(
            "Success", f"Article item created successfully with id {last_inserted_id}")

    def create_magazine_item(self, title, release_year, publisher, pages_count, language, genre):
        last_inserted_id = self.db.create_magazine_item(
            title, release_year, publisher, pages_count, language, genre)
        messagebox.showinfo(
            "Success", f"Magazine item created successfully with id {last_inserted_id}")

    def get_all_items(self):
        return self.db.get_all_items()

    def get_all_items_by_type(self, item_type):
        return self.db.get_all_items_by_type(item_type)

    def get_complete_item_details(self, item_id, item_type):
        return self.db.get_complete_item_details_by_id(item_id, item_type)

    def update_book_item(self, item_id, title, author, release_year):
        self.db.update_book_item(item_id, title, author, release_year)
        messagebox.showinfo(
            "Success", f"Book item with id {item_id} updated successfully")

    def update_article_item(self, item_id, title, author, release_year, abstract, word_count, language, keywords):
        self.db.update_article_item(
            item_id=item_id, title=title, author=author, release_year=release_year, abstract=abstract, word_count=word_count, language=language, keywords=keywords)
        messagebox.showinfo(
            "Success", f"Article item with id {item_id} updated successfully")

    def update_magazine_item(self, item_id, title, publisher, release_year, pages_count, language, genre):
        self.db.update_magazine_item(
            item_id=item_id, title=title, publisher=publisher, release_year=release_year, pages_count=pages_count, language=language, genre=genre)
        messagebox.showinfo(
            "Success", f"Magazine item with id {item_id} updated successfully")

    def update_student(self, student_id, registration, name, email, cpf, tel):
        self.db.update_student(student_id=student_id,
                               registration=registration,
                               name=name,
                               email=email,
                               cpf=cpf,
                               tel=tel
                               )

    def delete_item(self, item_id, item_type):
        self.db.delete_item(item_id=item_id, item_type=item_type)
        messagebox.showinfo(
            "Success", f"Item with id {item_id} deleted successfully")

    def reserve_item(self, item_id, student_id):
        self.db.reserve_item(item_id, student_id)
        messagebox.showinfo(
            "Success", f"Item with id {item_id} reserved by student with id {student_id}")

    def lend_item(self, item_id, student_id):
        self.db.lend_item(item_id, student_id)
        messagebox.showinfo(
            "Success", f"Item with id {item_id} lent to student with id {student_id}")

    def cancel_item_reservation(self, item_id):
        self.db.cancel_item_reservation(item_id)
        messagebox.showinfo(
            "Success", f"Reservation for item with id {item_id} cancelled")

    def return_item(self, item_id):
        self.db.return_item(item_id)
        messagebox.showinfo(
            "Success", f"Item with id {item_id} returned successfully")

    def close_connection(self):
        self.db.close_connection()
