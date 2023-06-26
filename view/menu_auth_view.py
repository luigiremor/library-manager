import customtkinter as ctk
from controller.library_controller import LibraryController
from view.menu_register import MenuRegister


class MenuAuth(ctk.CTkFrame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.buttons()
        self.entrys()
        self.labels()
        self.label_title()

    def label_title(self):
        self.lbl_title = ctk.CTkLabel(
            self, text="Login", font=("Arial", 20))
        self.lbl_title.grid(row=0, column=0, columnspan=2,
                            sticky="nsew", padx=10, pady=10)

    def buttons(self):
        self.btn_login = ctk.CTkButton(
            self, text="Login", command=self.login)
        self.btn_login.grid(row=3, column=0, columnspan=2,
                            sticky="ew", padx=10, pady=10)

        self.btn_register = ctk.CTkButton(
            self, text="Register", command=self.open_register_view)
        self.btn_register.grid(row=4, column=0, columnspan=2,
                               sticky="ew", padx=10, pady=10)

    def entrys(self):
        self.entry_username = ctk.CTkEntry(self)
        self.entry_username.grid(row=1, column=1, sticky="e", padx=10, pady=10)

        self.entry_password = ctk.CTkEntry(self, show="*")
        self.entry_password.grid(row=2, column=1, sticky="e", padx=10, pady=10)

    def labels(self):
        self.lbl_username = ctk.CTkLabel(self, text="Username:")
        self.lbl_username.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.lbl_password = ctk.CTkLabel(self, text="Password:")
        self.lbl_password.grid(row=2, column=0, sticky="w", padx=10, pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        is_logged = self.controller.login(username, password)
        if is_logged:
            self.close_window()

    def close_window(self):
        self.parent.show_view('menu_main')

    def open_register_view(self):
        self.parent.show_view('menu_register')
