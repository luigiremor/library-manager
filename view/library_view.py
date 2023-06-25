import tkinter
import customtkinter
from view.menu_auth_view import MenuAuth
from view.menu_collection_view import MenuCollection
from view.menu_lend_view import MenuLend
from view.menu_students_view import MenuStudents


class LibraryView(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.title("Library - System")
        self.geometry("1000x650")
        self.resizable(False, False)
        
        self.menu_auth = MenuAuth(self)
        self.menu_collection = MenuCollection(self)
        self.menu_students = MenuStudents(self)
        self.menu_lend = MenuLend(self)

        self.menu_auth.grid(row=0, column=0)
        self.menu_collection.grid(row=0, column=0)
        self.menu_lend.grid(row=0, column=0)
        self.menu_students.grid(row=0, column=0)

        self.show_menu_auth()

    

    def show_menu_auth(self):
        self.menu_collection.grid_remove()
        self.menu_lend.grid_remove()
        self.menu_students.grid_remove()
        self.menu_auth.grid()
    

    def show_menu_collection(self):
        self.menu_auth.grid_remove()
        self.menu_lend.grid_remove()
        self.menu_students.grid_remove()
        self.menu_collection.grid()
    

    def show_menu_lend(self):
        self.menu_auth.grid_remove()
        self.menu_collection.grid_remove()
        self.menu_students.grid_remove()
        self.menu_lend.grid()
    

    def show_menu_students(self):
        self.menu_auth.grid_remove()
        self.menu_collection.grid_remove()
        self.menu_lend.grid_remove()
        self.menu_students.grid()