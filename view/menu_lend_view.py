from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from components.ctk_listbox import CTkListbox
from controller.library_controller import LibraryController


class MenuLend(ctk.CTkFrame):

    key_to_string = {
        'id': 'ID',
        'id_item': 'ID Item',
        'title': 'Title',
        'release_year': 'Release Year',
        'is_lend': 'Available',
        'is_reserved': 'Reserved',
        'id_student_lent': 'Student Lent ID',
        'id_student_reserved': 'Student Reserved ID',
        'author': 'Author',
        'abstract': 'Abstract',
        'word_count': 'Word Count',
        'language': 'Language',
        'keywords': 'Keywords',
        'publisher': 'Publisher',
        'pages_count': 'Pages Count',
        'genre': 'Genre',
    }

    value_to_string = {
        0: 'Yes',
        1: 'No'
    }

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
        self.title_label = ctk.CTkLabel(self, text='Lend List')
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.go_back_button = ctk.CTkButton(
            self.buttons_frame, text='Go Back', command=lambda: self.parent.show_view('menu_main'))
        self.go_back_button.pack(side=tk.LEFT, padx=5)

        self.list_type_label = ctk.CTkLabel(
            self.buttons_frame, text='List Type')
        self.list_type_label.pack(side=tk.LEFT, padx=5)

        self.list_type_combobox = ctk.CTkComboBox(
            self.buttons_frame, values=['Book', 'Magazine', 'Article'], command=lambda event: self.refresh_items())

        self.list_type_combobox.pack(side=tk.LEFT, padx=5)
        self.list_type_combobox.set('Book')

        self.add_button = ctk.CTkButton(
            self.buttons_frame, text='New Lend', command=self.add_lend)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ctk.CTkButton(
            self.buttons_frame, text='Update Lend', command=self.update_lend)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ctk.CTkButton(
            self.buttons_frame, text='Delete Lend', command=self.delete_lend)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.items_listbox = CTkListbox(
            self, width=200, height=300, command=self.show_details)
        self.items_listbox.pack(fill=tk.BOTH, expand=True)

    def refresh_items(self):
        lends = self.controller.get_all_lendings()
        # messagebox.showinfo('Success', f'{lends}')
        self.items_listbox.clear()
        for index, item in enumerate(lends):
            lend_day = datetime.strptime(
                item['lend_date'], "%Y-%m-%d %H:%M:%S")
            return_day = datetime.strptime(
                item['return_date'], "%Y-%m-%d %H:%M:%S")
            days_until_return = (return_day - lend_day).days
            title = f'Protocolo: {item["id"]} | Item: {item["title"]}({item["id_item"]}) - Student: {item["name"]}({item["registration"]}) - Days Until Return: {days_until_return} days'
            self.items_listbox.insert(index, title, justify='left')

    def add_lend(self):
        AddLendForm(self)

    def update_lend(self):
        # Add your implementation for updating a lend here
        pass

    def delete_lend(self):
        # Add your implementation for deleting a lend here
        pass

    def show_details(self, event=None):
        # Clear the details frame
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected = self.items_listbox.get()
        item_type = self.list_type_combobox.get().lower()
        item_id = selected.split(' - ')[0]

        if item_id:
            details = self.controller.get_complete_item_details(
                item_id, item_type)
            for key, value in details.items():
                label = ctk.CTkLabel(self.details_frame,
                                     text=f"{self.key_to_string[key] if key in self.key_to_string else key}: {self.value_to_string[value] if value in self.value_to_string else value}")
                label.pack()


class AddLendForm(ctk.CTkToplevel):
    def __init__(self, parent: MenuLend):
        super().__init__(parent)
        self.title("New Lend")
        self.parent = parent
        self.item_type = parent.list_type_combobox.get()
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
