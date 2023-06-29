import customtkinter as ctk
import tkinter as tk
from components.ctk_listbox import CTkListbox

from controller.library_controller import LibraryController


class MenuCollection(ctk.CTkFrame):

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
        self.refresh_items('book')

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text='Library Collection')
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
            self.buttons_frame, values=['Book', 'Magazine', 'Article'], command=lambda event: self.refresh_items(self.list_type_combobox.get().lower()))

        self.list_type_combobox.pack(side=tk.LEFT, padx=5)
        self.list_type_combobox.set('Book')

        self.add_button = ctk.CTkButton(
            self.buttons_frame, text='Add Item', command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ctk.CTkButton(
            self.buttons_frame, text='Update Item', command=self.update_item)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ctk.CTkButton(
            self.buttons_frame, text='Delete Item', command=self.delete_item)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.items_listbox = CTkListbox(
            self, width=200, height=300, command=self.show_details)
        self.items_listbox.pack(fill=tk.BOTH, expand=True)

    def refresh_items(self, type_item):
        items = self.controller.get_all_items_by_type(type_item)
        self.items_listbox.clear()

        if not items:
            self.items_listbox.insert(0, 'No items found')
            return

        for index, item in enumerate(items):
            title = str(item['id_item']) + ' - ' + item['title'] + \
                ' | Available: ' + self.value_to_string[item['is_lend']]
            self.items_listbox.insert(index, title, justify='left')

    def add_item(self):
        from view.add_item_form import AddItemForm
        AddItemForm(self)

    def update_item(self):
        from view.update_item_form import UpdateItemForm
        UpdateItemForm(self)

    def delete_item(self):
        selected = self.items_listbox.get()
        item_type = self.list_type_combobox.get().lower()
        if selected:
            item_id = selected.split(' - ')[0]
            self.controller.delete_item(item_id=item_id, item_type=item_type)
            self.refresh_items(item_type)

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
