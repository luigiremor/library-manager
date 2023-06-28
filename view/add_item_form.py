import customtkinter as ctk
import tkinter as tk

from controller.library_controller import LibraryController
from view.menu_collection_view import MenuCollection


class AddItemForm(ctk.CTkToplevel):
    def __init__(self, parent: MenuCollection):
        super().__init__(parent)
        self.title("New Item")
        self.parent = parent
        self.item_type = parent.list_type_combobox.get()
        self.controller: LibraryController = parent.controller

        self.select_label = ctk.CTkLabel(self, text="Select Item Type")
        self.select_label.pack(fill=tk.X, padx=5, pady=5)

        self.create_form_for_item_type(self.item_type)

    def create_form_for_item_type(self, item_type):
        # Remove all current widgets
        for widget in self.winfo_children():
            if widget != self.select_label and widget != self.item_type_combobox:
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
        self.controller.create_book_item(title, release_year, author)

        self.parent.refresh_items(self.item_type)

        self.destroy()

    def create_magazine_item(self):
        title = self.title_entry.get()
        release_year = self.release_year_entry.get()
        publisher = self.publisher_entry.get()
        pages_count = self.pages_count_entry.get()
        language = self.language_entry.get()
        genre = self.genre_entry.get()
        self.controller.create_magazine_item(
            title, release_year, publisher, pages_count, language, genre)

        self.parent.refresh_items(self.item_type)

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

        self.parent.refresh_items(self.item_type)

        self.destroy()
