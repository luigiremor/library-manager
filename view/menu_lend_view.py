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

        self.add_button = ctk.CTkButton(
            self.buttons_frame, text='Lend Item', command=self.add_lend)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.return_button = ctk.CTkButton(
            self.buttons_frame, text='Return Item', command=self.return_lend)
        self.return_button.pack(side=tk.LEFT, padx=5)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.items_listbox = CTkListbox(
            self, width=900, height=300, command=self.show_details)
        self.items_listbox.pack(fill=tk.BOTH, expand=True)

        self.refresh_items()

    def refresh_items(self):
        lends = self.controller.get_all_lendings()
        self.items_listbox.clear()
        if not lends:
            self.items_listbox.insert(0, 'No lends found')
            return

        for index, item in enumerate(lends):
            today = datetime.today()
            return_day = datetime.strptime(
                item['return_date'], "%Y-%m-%d %H:%M:%S")
            days_until_return = (return_day - today).days
            title = f'Protocolo: {item["id"]} | Título: {item["title"]}({item["id_item"]}) - Student: {item["name"]}({item["registration"]}) - Days Until Return: {days_until_return} days'
            self.items_listbox.insert(index, title, justify='left')

    def add_lend(self):
        from view.add_lend_form import AddLendForm
        AddLendForm(self)

    def return_lend(self):
        selected = self.items_listbox.get()
        item_id = selected.split(' | ')[0].split(':')[1].strip()

        if item_id:
            self.controller.return_item(item_id)
            self.refresh_items()

    def show_details(self, event=None):
        # Clear the details frame
        for widget in self.details_frame.winfo_children():
            widget.destroy()
