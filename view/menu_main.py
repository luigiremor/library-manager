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

    def navbar(self):
        # Create a Frame to hold all buttons
        navbar_frame = tk.Frame(self, bg=self['bg'])

        self.btn_home = ctk.CTkButton(
            navbar_frame, text="Home", command=self.go_home)
        self.btn_home.grid(row=0, column=0, padx=10, pady=10)

        self.btn_lend = ctk.CTkButton(
            navbar_frame, text="Lend", command=self.go_lend)
        self.btn_lend.grid(row=0, column=1, padx=10, pady=10)

        self.btn_collection = ctk.CTkButton(
            navbar_frame, text="Collection", command=self.go_collection)
        self.btn_collection.grid(row=0, column=2, padx=10, pady=10)

        self.btn_students = ctk.CTkButton(
            navbar_frame, text="Students", command=self.go_student)
        self.btn_students.grid(row=0, column=3, padx=10, pady=10)

        self.btn_logout = ctk.CTkButton(
            navbar_frame, text="Logout", command=self.exit)
        self.btn_logout.grid(row=0, column=4, padx=10, pady=10)

        navbar_frame.place(anchor="n", relx=0.5)

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

        window_width = self.parent.winfo_width()
        window_height = self.parent.winfo_height()

        image = Image.open("view/images/ufsc2.png")

        width = 300
        height = 300
        image = image.resize((width, height), Image.ANTIALIAS)

        logo = ImageTk.PhotoImage(image)

        self.label_logo = tk.Label(self, image=logo)

        image_x = window_width // 2
        image_y = window_height * 0.4
        self.label_logo.place(x=image_x, y=image_y, anchor="center")
        center_x = window_width // 2
        image_y = window_height * 0.5
        self.label_logo.place(x=center_x, y=image_y, anchor="center")

        self.label_logo.configure(bg=self["bg"])

        self.label_logo.image = logo
        self.label_logo["highlightthickness"] = 0
