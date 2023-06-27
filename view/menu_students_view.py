import tkinter as tk
import customtkinter 
from controller.library_controller import LibraryController


class MenuStudents(customtkinter.CTkFrame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent, height=650, width=1000)
        self.parent = parent
        self.controller = controller
        self.buttons()
        self.entrys()
    
    
    def buttons(self):
        self.btn_register = customtkinter.CTkButton(self, text="Delete Student", command=None)
        self.btn_register.grid(row=4, column=1, sticky="e", padx=10, pady=10)
        self.btn_back = customtkinter.CTkButton(self, text="Back", command=None)
        self.btn_back.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.btn_register = customtkinter.CTkButton(self, text="Edit Student", command=None)
        self.btn_register.grid(row=4, column=2, sticky="e", padx=10, pady=10)
        

    def entrys(self):
        self.entry1 = customtkinter.CTkEntry(self, width=150, corner_radius=6, placeholder_text="Register Student")
        self.entry1.grid(row=1, column=1, sticky="e", padx=10, pady=10)


    def labels(self):
        self.lbl_title = customtkinter.CTkLabel(self, text="Students", font=("Arial", 20))
        self.lbl_title.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.lbl_name = customtkinter.CTkLabel(self, text="Name:")
        self.lbl_name.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.lbl_email = customtkinter.CTkLabel(self, text="Email:")
        self.lbl_email.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.lbl_password = customtkinter.CTkLabel(self, text="Password:")
        self.lbl_password.grid(row=3, column=0, sticky="w", padx=10, pady=10)

        

        

        
        
        