import tkinter as tk
from tkinter import messagebox
import customtkinter
from components.ctk_listbox import CTkListbox
from controller.library_controller import LibraryController


class MenuLend(customtkinter.CTkFrame):
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
        self.title_label = customtkinter.CTkLabel(self, text='Lend List')
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.buttons_frame = customtkinter.CTkFrame(self)
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.refresh_button = customtkinter.CTkButton(
            self.buttons_frame, text='Go back', command=lambda: self.parent.show_view('menu_main'))
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.new_button = customtkinter.CTkButton(
            self.buttons_frame, text='New Lend', command=None)
        self.new_button.pack(side=tk.LEFT, padx=5)

        self.update_button = customtkinter.CTkButton(
            self.buttons_frame, text='Update Lend', command=None)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = customtkinter.CTkButton(
            self.buttons_frame, text='Delete Lend', command=None)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.details_frame = customtkinter.CTkFrame(self)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        students = [
            f"{student['registration']} - {student['name']}" for student in self.controller.get_all_students()]

        self.students_combobox = customtkinter.CTkComboBox(
            self.details_frame, values=students, command=None)
        self.students_combobox.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        self.item_type_combobox = customtkinter.CTkComboBox(
            self.details_frame, values=['Book', 'Magazine', 'Article'], command=self.update_items_combobox)
        self.item_type_combobox.set('Book')
        self.item_type_combobox.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        self.items_combobox = customtkinter.CTkComboBox(
            self.details_frame, values=[], command=None)
        self.items_combobox.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

    def update_items_combobox(self, event=None):
        selected_type = self.item_type_combobox.get()
        items = self.controller.get_all_items_by_type(selected_type)

        # Check if items is not None before the list comprehension
        if items:
            items_values = [
                f"{item['id_item']} - {item['title']}" for item in items]

            self.items_combobox.destroy()
            self.items_combobox = customtkinter.CTkComboBox(
                self.details_frame, values=items_values, command=None)
        else:
            self.items_combobox.destroy()
            self.items_combobox = customtkinter.CTkComboBox(
                self.details_frame, values=[f'No {selected_type} available'], command=None)
        self.items_combobox.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
