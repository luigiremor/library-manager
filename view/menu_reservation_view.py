import tkinter as tk
import customtkinter
from components.ctk_listbox import CTkListbox
from controller.library_controller import LibraryController


class MenuReservation(customtkinter.CTkFrame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.grid(sticky="nsew")

        # configure grid to fill window
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.title_label = customtkinter.CTkLabel(
            self, text='Reservation List')
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.buttons_frame = customtkinter.CTkFrame(self)
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.refresh_button = customtkinter.CTkButton(
            self.buttons_frame, text='Refresh', command=None)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.new_button = customtkinter.CTkButton(
            self.buttons_frame, text='Add Reservation', command=None)
        self.new_button.pack(side=tk.LEFT, padx=5)

        self.update_button = customtkinter.CTkButton(
            self.buttons_frame, text='Update Reservation', command=None)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = customtkinter.CTkButton(
            self.buttons_frame, text='Delete Reservation', command=None)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.details_frame = customtkinter.CTkFrame(self)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.lends_listbox = CTkListbox(
            self, width=200, height=300, command=None)
        self.lends_listbox.pack(fill=tk.BOTH, expand=True)
