from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from components.ctk_listbox import CTkListbox
from controller.library_controller import LibraryController


class MenuReservation(ctk.CTkFrame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.grid(sticky="nsew")

        # configure grid to fill window
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 0, weight=1)

        self.create_widgets()
        self.refresh_items()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text='Reservation List')
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.go_back_button = ctk.CTkButton(
            self.buttons_frame, text='Go Back', command=lambda: self.parent.show_view('menu_main'))
        self.go_back_button.pack(side=tk.LEFT, padx=5)

        self.add_button = ctk.CTkButton(
            self.buttons_frame, text='Add Reservation', command=self.add_reservation)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ctk.CTkButton(
            self.buttons_frame, text='Cancel Reservation', command=self.remove_reservation)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.items_listbox = CTkListbox(
            self, width=900, height=300, command=self.show_details)
        self.items_listbox.pack(fill=tk.BOTH, expand=True)

        self.refresh_items()

    def refresh_items(self):
        reservations = self.controller.get_all_reservations()
        self.items_listbox.clear()
        if not reservations:
            self.items_listbox.insert(0, 'No reservations found')
            return

        for index, item in enumerate(reservations):
            title = f'Protocolo: {item["id"]} | Título: {item["title"]}({item["id_item"]}) - Student: {item["name"]}({item["registration"]}) - Status: {item["status"]}'
            self.items_listbox.insert(index, title, justify='left')

    def add_reservation(self):
        # from view.add_reservation_form import AddReservationForm
        # AddReservationForm(self)
        pass

    def remove_reservation(self):
        selected = self.items_listbox.get()
        item_id = selected.split(' | ')[0].split(':')[1].strip()

        if item_id:
            self.controller.remove_reservation(item_id)
            self.refresh_items()

    def show_details(self, event=None):
        # Clear the details frame
        for widget in self.details_frame.winfo_children():
            widget.destroy()
