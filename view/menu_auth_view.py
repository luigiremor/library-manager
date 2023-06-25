import tkinter
import customtkinter

class MenuAuth(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=650, width=1000)
        self.parent = parent
        self.buttons()
        self.entrys()
        self.labels()


    def buttons(self):
        self.btn_login = customtkinter.CTkButton(self, text="Login", command=None)
        self.btn_login.grid(row=3, column=0, sticky="w", padx=10, pady=10)

        self.btn_register = customtkinter.CTkButton(self, text="Register", command=None)
        self.btn_register.grid(row=3, column=1, sticky="e", padx=10, pady=10)
    

    
    def entrys(self):
        self.entry_username = customtkinter.CTkEntry(self)
        self.entry_username.grid(row=1, column=1, sticky="e", padx=10, pady=10)

        self.entry_password = customtkinter.CTkEntry(self, show="*")
        self.entry_password.grid(row=2, column=1, sticky="e", padx=10, pady=10)
    

    
    def labels(self):
        self.lbl_username = customtkinter.CTkLabel(self, text="Username:")
        self.lbl_username.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.lbl_password = customtkinter.CTkLabel(self, text="Password:")
        self.lbl_password.grid(row=2, column=0, sticky="w", padx=10, pady=10)
    