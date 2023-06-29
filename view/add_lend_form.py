from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from components.ctk_listbox import CTkListbox
from controller.library_controller import LibraryController
from view.menu_lend_view import MenuLend


class AddLendForm(ctk.CTkToplevel):
    def __init__(self, parent: MenuLend):
        super().__init__(parent)
        self.title("Add Lend")
        self.parent = parent
        self.controller: LibraryController = parent.controller

        self.select_label = ctk.CTkLabel(self, text="Select Item Type")
        self.select_label.pack(fill=tk.X, padx=5, pady=5)

        self.student_label = ctk.CTkLabel(self, text="Student")
        self.student_label.pack(fill=tk.X, padx=5, pady=5)

        students = [
            f"{student['registration']} - {student['name']}" for student in self.controller.get_all_students()]

        self.student_combobox = ctk.CTkComboBox(
            self, values=students)
        self.student_combobox.pack(fill=tk.X, padx=5, pady=5)

        self.item_type_combobox = ctk.CTkComboBox(
            self, values=['Book', 'Magazine', 'Article'], command=self.update_items_combobox)
        self.item_type_combobox.set('Book')
        self.item_type_combobox.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        self.items_combobox = ctk.CTkComboBox(
            self, values=[], command=None)
        self.items_combobox.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        self.add_button = ctk.CTkButton(
            self, text='Add Lend', command=self.add_lend)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

    def add_lend(self):
        student_registration = self.student_combobox.get().split(' - ')[0]
        student = self.controller.get_student_by_registration(
            registration=student_registration)
        item_id = self.items_combobox.get().split(' - ')[0]
        self.controller.lend_item(
            item_id=item_id, student_id=student['id'])
        self.parent.refresh_items()
        self.destroy()

    def update_items_combobox(self, event=None):
        selected_type = self.item_type_combobox.get()
        items = self.controller.get_all_items_by_type(selected_type)

        if items:
            items_values = list()
            for item in items:
                if item['is_lend'] != 1:  # Check if item is not lend
                    items_values.append(f"{item['id_item']} - {item['title']}")

            self.items_combobox.destroy()
            self.items_combobox = ctk.CTkComboBox(
                self, values=items_values, command=None)
        else:
            self.items_combobox.destroy()
            self.items_combobox = ctk.CTkComboBox(
                self, values=[f'No {selected_type} available'], command=None)
        self.items_combobox.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
