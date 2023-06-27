import customtkinter as ctk
import tkinter as tk
from components.ctk_listbox import CTkListbox

from controller.library_controller import LibraryController


class MenuCollection(ctk.CTkFrame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Create and pack the widgets
        self.title_label = ctk.CTkLabel(self, text='Library Collection')
        self.title_label.grid(row=0, column=0, columnspan=4)

        # Button to refresh the items list
        self.refresh_button = ctk.CTkButton(
            self, text='Refresh', command=self.refresh_items)
        self.refresh_button.grid(row=1, column=0)

        # Button to create a new item
        self.new_button = ctk.CTkButton(
            self, text='New Item', command=self.new_item)
        self.new_button.grid(row=1, column=1)

        # Entry and button to update an existing item
        self.update_entry = ctk.CTkEntry(self)
        self.update_entry.grid(row=1, column=2)
        self.update_button = ctk.CTkButton(
            self, text='Update Item', command=self.update_item)
        self.update_button.grid(row=1, column=3)

        # Entry and button to delete an item
        self.delete_entry = ctk.CTkEntry(self)
        self.delete_entry.grid(row=2, column=2)
        self.delete_button = ctk.CTkButton(
            self, text='Delete Item', command=self.delete_item)
        self.delete_button.grid(row=2, column=3)

        # Listbox to display all items
        self.items_listbox = CTkListbox(self)
        self.items_listbox.grid(row=3, column=0, columnspan=4)

    def refresh_items(self):
        # Get all items from the controller
        items = self.controller.get_all_items()

        # Clear the listbox
        self.items_listbox.delete(0, tk.END)

        # Insert each item into the listbox
        for item in items:
            self.items_listbox.insert(tk.END, item)

    def new_item(self):
        # Create a new item using a method in your controller
        # This will depend on what data is needed to create an item
        pass

    def update_item(self):
        # Get the selected item
        selected = self.update_entry.get()

        # Update the item using a method in your controller
        # This will depend on what data is needed to update an item
        pass

    def delete_item(self):
        # Get the selected item
        selected = self.delete_entry.get()

        # Delete the item using the controller
        self.controller.delete_item(selected)

        # Refresh the items list
        self.refresh_items()
