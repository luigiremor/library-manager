from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from components.ctk_listbox import CTkListbox

from controller.library_controller import LibraryController


class MenuCollection(ctk.CTkFrame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent)
        self.controller = controller
        self.grid(sticky="nsew")

        # configure grid to fill window
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text='Library Collection')
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.list_type_label = ctk.CTkLabel(
            self.buttons_frame, text='List Type')
        self.list_type_label.pack(side=tk.LEFT, padx=5)

        self.list_type_combobox = ctk.CTkComboBox(
            self.buttons_frame, values=['Book', 'Magazine', 'Article'])

        self.list_type_combobox.pack(side=tk.LEFT, padx=5)
        self.list_type_combobox.set('Book')

        self.refresh_button = ctk.CTkButton(
            self.buttons_frame, text='Refresh', command=lambda: self.refresh_items(self.list_type_combobox.get().lower()))
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.new_button = ctk.CTkButton(
            self.buttons_frame, text='New Item', command=self.new_item)
        self.new_button.pack(side=tk.LEFT, padx=5)

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
        for index, item in enumerate(items):
            title = str(item['id_item']) + ' - ' + item['title']
            self.items_listbox.insert(index, title)

    def new_item(self):
        NewItemForm(self)

    def update_item(self):
        selected = self.items_listbox.get()
        if selected:
            UpdateItemForm(self, selected)

    def delete_item(self):
        selected = self.items_listbox.get()
        if selected:
            self.controller.delete_item(selected)
            self.refresh_items()

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
                                     text=f"{key}: {value}")
                label.pack()

    # def key_to_string(self, key):
    #     return key.replace('_', ' ').capitalize()

    # def string_to_key(self, string):
    #     return string.replace(' ', '_').lower()


class NewItemForm(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("New Item")
        self.controller: LibraryController = parent.controller

        self.select_label = ctk.CTkLabel(self, text="Select Item Type")
        self.select_label.pack(fill=tk.X, padx=5, pady=5)

        self.item_type = tk.StringVar()
        self.item_type.set("Book")
        self.item_type_combobox = ctk.CTkComboBox(
            self, width=200, height=30, variable=self.item_type, state="readonly", values=["Book", "Magazine", "Article"])
        self.item_type_combobox.pack(fill=tk.X, padx=5, pady=5)
        self.item_type_combobox.bind(
            '<<ComboboxSelected>>', self.on_item_type_change)

        # initially create form for 'Book'
        self.create_form_for_item_type('Book')

    def on_item_type_change(self, event=None):
        self.create_form_for_item_type(self.item_type.get())

    def create_form_for_item_type(self, item_type):
        # Remove all current widgets
        for widget in self.winfo_children():
            if widget != self.select_label and widget != self.item_type_combobox and widget != self.create_button:
                widget.destroy()
        # Depending on the item_type, create a different form
        if item_type == 'Book':
            self.book_form()
        elif item_type == 'Magazine':
            self.magazine_form()
        elif item_type == 'Article':
            self.article_form()

    def book_form(self):
        self.title_label = ctk.CTkLabel(self, text="Title")
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.pack(fill=tk.X, padx=5, pady=5)

        self.release_year_label = ctk.CTkLabel(self, text="Release Year")
        self.release_year_label.pack(fill=tk.X, padx=5, pady=5)

        self.release_year_entry = ctk.CTkEntry(self)
        self.release_year_entry.pack(fill=tk.X, padx=5, pady=5)

        self.author_label = ctk.CTkLabel(self, text="Author")
        self.author_label.pack(fill=tk.X, padx=5, pady=5)

        self.author_entry = ctk.CTkEntry(self)
        self.author_entry.pack(fill=tk.X, padx=5, pady=5)

        self.create_button = ctk.CTkButton(
            self, text="Create", command=self.create_book_item)
        self.create_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def magazine_form(self):
        self.title_label = ctk.CTkLabel(self, text="Title")
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.pack(fill=tk.X, padx=5, pady=5)

        self.release_year_label = ctk.CTkLabel(self, text="Release Year")
        self.release_year_label.pack(fill=tk.X, padx=5, pady=5)

        self.release_year_entry = ctk.CTkEntry(self)
        self.release_year_entry.pack(fill=tk.X, padx=5, pady=5)

        self.publisher_label = ctk.CTkLabel(self, text="Publisher")
        self.publisher_label.pack(fill=tk.X, padx=5, pady=5)

        self.publisher_entry = ctk.CTkEntry(self)
        self.publisher_entry.pack(fill=tk.X, padx=5, pady=5)

        self.pages_count_label = ctk.CTkLabel(self, text="Pages Count")
        self.pages_count_label.pack(fill=tk.X, padx=5, pady=5)

        self.pages_count_entry = ctk.CTkEntry(self)
        self.pages_count_entry.pack(fill=tk.X, padx=5, pady=5)

        self.language_label = ctk.CTkLabel(self, text="Language")
        self.language_label.pack(fill=tk.X, padx=5, pady=5)

        self.language_entry = ctk.CTkEntry(self)
        self.language_entry.pack(fill=tk.X, padx=5, pady=5)

        self.genre_label = ctk.CTkLabel(self, text="Genre")
        self.genre_label.pack(fill=tk.X, padx=5, pady=5)

        self.genre_entry = ctk.CTkEntry(self)
        self.genre_entry.pack(fill=tk.X, padx=5, pady=5)

        self.create_button = ctk.CTkButton(
            self, text="Create", command=self.create_magazine_item)
        self.create_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def article_form(self):
        self.title_label = ctk.CTkLabel(self, text="Title")
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.pack(fill=tk.X, padx=5, pady=5)

        self.release_year_label = ctk.CTkLabel(self, text="Release Year")
        self.release_year_label.pack(fill=tk.X, padx=5, pady=5)

        self.release_year_entry = ctk.CTkEntry(self)
        self.release_year_entry.pack(fill=tk.X, padx=5, pady=5)

        self.abstract_label = ctk.CTkLabel(self, text="Abstract")
        self.abstract_label.pack(fill=tk.X, padx=5, pady=5)

        self.abstract_entry = ctk.CTkEntry(self)
        self.abstract_entry.pack(fill=tk.X, padx=5, pady=5)

        self.word_count_label = ctk.CTkLabel(self, text="Word Count")
        self.word_count_label.pack(fill=tk.X, padx=5, pady=5)

        self.word_count_entry = ctk.CTkEntry(self)
        self.word_count_entry.pack(fill=tk.X, padx=5, pady=5)

        self.author_label = ctk.CTkLabel(self, text="Author")
        self.author_label.pack(fill=tk.X, padx=5, pady=5)

        self.author_entry = ctk.CTkEntry(self)
        self.author_entry.pack(fill=tk.X, padx=5, pady=5)

        self.language_label = ctk.CTkLabel(self, text="Language")
        self.language_label.pack(fill=tk.X, padx=5, pady=5)

        self.language_entry = ctk.CTkEntry(self)
        self.language_entry.pack(fill=tk.X, padx=5, pady=5)

        self.keywords_label = ctk.CTkLabel(self, text="Keywords")
        self.keywords_label.pack(fill=tk.X, padx=5, pady=5)

        self.keywords_entry = ctk.CTkEntry(self)
        self.keywords_entry.pack(fill=tk.X, padx=5, pady=5)

        self.create_button = ctk.CTkButton(
            self, text="Create", command=self.create_article_item)
        self.create_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def create_book_item(self):
        title = self.title_entry.get()
        release_year = self.release_year_entry.get()
        author = self.author_entry.get()
        self.controller.create_book_item(title, author, release_year)
        self.destroy()

    def create_magazine_item(self):
        title = self.title_entry.get()
        release_year = self.release_year_entry.get()
        publisher = self.publisher_entry.get()
        pages_count = self.pages_count_entry.get()
        language = self.language_entry.get()
        genre = self.genre_entry.get()
        messagebox.showinfo(
            "Info", f'{title} {release_year} {publisher} {pages_count} {language} {genre}')
        self.controller.create_magazine_item(
            title, release_year, publisher, pages_count, language, genre)
        self.destroy()

    def create_article_item(self):
        title = self.title_entry.get()
        release_year = self.release_year_entry.get()
        abstract = self.abstract_entry.get()
        word_count = self.word_count_entry.get()
        author = self.author_entry.get()
        language = self.language_entry.get()
        keywords = self.keywords_entry.get()
        self.controller.create_article_item(
            title, release_year, abstract, word_count, author, language, keywords)
        self.destroy()


class UpdateItemForm(ctk.CTkToplevel):
    def __init__(self, parent, item):
        super().__init__(parent)
        self.title("Update Item")
        self.controller = parent.controller
        self.item = item

        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.insert(0, item)
        self.title_entry.pack(fill=tk.X, padx=5, pady=5)

        self.update_button = ctk.CTkButton(
            self, text="Update", command=self.update_item)
        self.update_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def update_item(self):
        new_title = self.title_entry.get()
        self.controller.update_item(self.item, new_title)
        self.destroy()
