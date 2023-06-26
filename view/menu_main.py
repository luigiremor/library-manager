import customtkinter as ctk

from controller.library_controller import LibraryController


class MenuMain(ctk.CTkFrame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.navbar()

    def navbar(self):
        self.btn_lend = ctk.CTkButton(
            self, text="Lend", command=None)
        self.btn_lend.grid(row=0, column=0, padx=10, pady=10)

        self.btn_return = ctk.CTkButton(
            self, text="Return", command=None)
        self.btn_return.grid(row=0, column=1, padx=10, pady=10)

        self.btn_search = ctk.CTkButton(
            self, text="Search", command=None)
        self.btn_search.grid(row=0, column=2, padx=10, pady=10)

        self.btn_add = ctk.CTkButton(
            self, text="Add", command=None)
        self.btn_add.grid(row=0, column=3, padx=10, pady=10)

        self.btn_remove = ctk.CTkButton(
            self, text="Remove", command=None)
        self.btn_remove.grid(row=0, column=4, padx=10, pady=10)

        self.btn_logout = ctk.CTkButton(
            self, text="Logout", command=None)
        self.btn_logout.grid(row=0, column=5, padx=10, pady=10)
