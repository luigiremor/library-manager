import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from controller.library_controller import LibraryController



class MenuMain(ctk.CTkFrame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.navbar()
        self.widgets()
        self.images()

    def navbar(self):
        self.btn_lend = ctk.CTkButton(
            self, text="Home", command=self.go_home)
        self.btn_lend.grid(row=0, column=0, padx=10, pady=10)

        self.btn_lend = ctk.CTkButton(
            self, text="Lend", command=self.go_lend)
        self.btn_lend.grid(row=0, column=1, padx=10, pady=10)

        self.btn_collection = ctk.CTkButton(
            self, text="Collection", command=self.go_collection)
        self.btn_collection.grid(row=0, column=2, padx=10, pady=10)

        self.btn_students = ctk.CTkButton(
            self, text="Students", command=self.go_student)
        self.btn_students.grid(row=0, column=3, padx=10, pady=10)

        self.btn_add = ctk.CTkButton(
            self, text="Add", command=None)
        self.btn_add.grid(row=0, column=4, padx=10, pady=10)

        self.btn_logout = ctk.CTkButton(
            self, text="Logout", command=self.exit)
        self.btn_logout.grid(row=0, column=6, padx=10, pady=10)

    def go_home(self):
        self.parent.show_view("menu_main")

    def exit(self):
        self.parent.show_view("menu_auth")

    def go_collection(self):
        self.parent.show_view("menu_collection")

    def go_student(self):
        self.parent.show_view("menu_students")

    def go_lend(self):
        self.parent.show_view("menu_lend")

    def widgets(self):
        self.label = ctk.CTkLabel(self, text="Biblioteca Universitária", font=("Arial", 30))
        self.label.place(x=330, y=500)

    def images(self):
        image = Image.open("view/images/ufsc2.png")

        width = 300  
        height = 300 
        image = image.resize((width, height), Image.ANTIALIAS)

        logo = ImageTk.PhotoImage(image)

        self.label_logo = tk.Label(self, image=logo)
        self.label_logo.place(x=450, y=245)

        self.label_logo.configure(bg=self["bg"])

        self.label_logo.image = logo  
        self.label_logo["highlightthickness"] = 0