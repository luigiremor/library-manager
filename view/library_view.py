import tkinter
import customtkinter

class LibraryView:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.window = customtkinter.CTk()
        self.window.title("Library Management System")
        self.window.geometry("1000x650")
        self.window.resizable(False, False)
        self.window.mainloop()

    def menu_auth():
        pass

    def menu_collection():
        pass

    def menu_lend():
        pass

    def menu_students():
        pass

a = LibraryView()