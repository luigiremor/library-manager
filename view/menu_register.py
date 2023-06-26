import customtkinter as ctk

from controller.library_controller import LibraryController


class MenuRegister(ctk.CTkFrame):
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
            self, text="Register Librarian", font=("Arial", 20))
        self.lbl_title.grid(row=0, column=0, columnspan=2,
                            sticky="nsew", padx=10, pady=10)

    def buttons(self):
        self.btn_register = ctk.CTkButton(
            self, text="Register", command=self.register_librarian)
        self.btn_register.grid(row=4, column=1, sticky="e", padx=10, pady=10)

        self.btn_back = ctk.CTkButton(
            self, text="Back", command=self.close_window)
        self.btn_back.grid(row=4, column=0, sticky="w", padx=10, pady=10)

    def entrys(self):
        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.grid(row=1, column=1, sticky="e", padx=10, pady=10)

        self.entry_email = ctk.CTkEntry(self)
        self.entry_email.grid(row=2, column=1, sticky="e", padx=10, pady=10)

        self.entry_password = ctk.CTkEntry(self, show="*")
        self.entry_password.grid(row=3, column=1, sticky="e", padx=10, pady=10)

    def labels(self):
        self.lbl_name = ctk.CTkLabel(self, text="Name:")
        self.lbl_name.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.lbl_email = ctk.CTkLabel(self, text="Email:")
        self.lbl_email.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.lbl_password = ctk.CTkLabel(self, text="Password:")
        self.lbl_password.grid(row=3, column=0, sticky="w", padx=10, pady=10)

    def register_librarian(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        is_created = self.controller.create_librarian(name, email, password)

        if is_created:
            self.close_window()

    def close_window(self):
        self.parent.show_view('menu_auth')  # use 'menu_auth' as the argument
