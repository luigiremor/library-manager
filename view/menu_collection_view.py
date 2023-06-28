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
        self.refresh_items('book')

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text='Library Collection')
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.list_type_label = ctk.CTkLabel(
            self.buttons_frame, text='List Type')
        self.list_type_label.pack(side=tk.LEFT, padx=5)

        self.list_type_combobox = ctk.CTkComboBox(
            self.buttons_frame, values=['Book', 'Magazine', 'Article'], command=lambda event: self.refresh_items(self.list_type_combobox.get().lower()))

        self.list_type_combobox.pack(side=tk.LEFT, padx=5)
        self.list_type_combobox.set('Book')

        self.new_button = ctk.CTkButton(
            self.buttons_frame, text='New Item', command=self.add_item)
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

    def add_item(self):
        AddItemForm(self)

    def update_item(self):
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
                                     text=f"{key}: {value}")
                label.pack()


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


class UpdateItemForm(ctk.CTkToplevel):
    def __init__(self, parent: MenuCollection):
        super().__init__(parent)
        self.item_type = parent.list_type_combobox.get()
        self.parent = parent

        self.title("New Item")

        self.controller: LibraryController = parent.controller

        self.select_label = ctk.CTkLabel(self, text="Select Item Type")
        self.select_label.pack(fill=tk.X, padx=5, pady=5)

        self.selected_item_id = parent.items_listbox.get().split(' - ')[0]

        self.item_data = self.controller.get_complete_item_details(
            self.selected_item_id, self.item_type.lower())

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
        self.title_entry.insert(0, self.item_data['title'])

        self.release_year_label = ctk.CTkLabel(self, text="Release Year")
        self.release_year_label.pack(fill=tk.X, padx=5, pady=5)

        self.release_year_entry = ctk.CTkEntry(self)
        self.release_year_entry.pack(fill=tk.X, padx=5, pady=5)
        self.release_year_entry.insert(0, self.item_data['release_year'])

        self.author_label = ctk.CTkLabel(self, text="Author")
        self.author_label.pack(fill=tk.X, padx=5, pady=5)

        self.author_entry = ctk.CTkEntry(self)
        self.author_entry.pack(fill=tk.X, padx=5, pady=5)
        self.author_entry.insert(0, self.item_data['author'])

        self.create_button = ctk.CTkButton(
            self, text="Update Book", command=self.update_book_item)
        self.create_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def magazine_form(self):
        self.title_label = ctk.CTkLabel(self, text="Title")
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.pack(fill=tk.X, padx=5, pady=5)
        self.title_entry.insert(0, self.item_data['title'])

        self.release_year_label = ctk.CTkLabel(self, text="Release Year")
        self.release_year_label.pack(fill=tk.X, padx=5, pady=5)

        self.release_year_entry = ctk.CTkEntry(self)
        self.release_year_entry.pack(fill=tk.X, padx=5, pady=5)
        self.release_year_entry.insert(0, self.item_data['release_year'])

        self.publisher_label = ctk.CTkLabel(self, text="Publisher")
        self.publisher_label.pack(fill=tk.X, padx=5, pady=5)

        self.publisher_entry = ctk.CTkEntry(self)
        self.publisher_entry.pack(fill=tk.X, padx=5, pady=5)
        self.publisher_entry.insert(0, self.item_data['publisher'])

        self.pages_count_label = ctk.CTkLabel(self, text="Pages Count")
        self.pages_count_label.pack(fill=tk.X, padx=5, pady=5)

        self.pages_count_entry = ctk.CTkEntry(self)
        self.pages_count_entry.pack(fill=tk.X, padx=5, pady=5)
        self.pages_count_entry.insert(0, self.item_data['pages_count'])

        self.language_label = ctk.CTkLabel(self, text="Language")
        self.language_label.pack(fill=tk.X, padx=5, pady=5)

        self.language_entry = ctk.CTkEntry(self)
        self.language_entry.pack(fill=tk.X, padx=5, pady=5)
        self.language_entry.insert(0, self.item_data['language'])

        self.genre_label = ctk.CTkLabel(self, text="Genre")
        self.genre_label.pack(fill=tk.X, padx=5, pady=5)

        self.genre_entry = ctk.CTkEntry(self)
        self.genre_entry.pack(fill=tk.X, padx=5, pady=5)
        self.genre_entry.insert(0, self.item_data['genre'])

        self.create_button = ctk.CTkButton(
            self, text="Update Magazine", command=self.update_magazine_item)
        self.create_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def article_form(self):
        self.title_label = ctk.CTkLabel(self, text="Title")
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.pack(fill=tk.X, padx=5, pady=5)
        self.title_entry.insert(0, self.item_data['title'])

        self.release_year_label = ctk.CTkLabel(self, text="Release Year")
        self.release_year_label.pack(fill=tk.X, padx=5, pady=5)

        self.release_year_entry = ctk.CTkEntry(self)
        self.release_year_entry.pack(fill=tk.X, padx=5, pady=5)
        self.release_year_entry.insert(0, self.item_data['release_year'])

        self.abstract_label = ctk.CTkLabel(self, text="Abstract")
        self.abstract_label.pack(fill=tk.X, padx=5, pady=5)

        self.abstract_entry = ctk.CTkEntry(self)
        self.abstract_entry.pack(fill=tk.X, padx=5, pady=5)
        self.abstract_entry.insert(0, self.item_data['abstract'])

        self.word_count_label = ctk.CTkLabel(self, text="Word Count")
        self.word_count_label.pack(fill=tk.X, padx=5, pady=5)

        self.word_count_entry = ctk.CTkEntry(self)
        self.word_count_entry.pack(fill=tk.X, padx=5, pady=5)
        self.word_count_entry.insert(0, self.item_data['word_count'])

        self.author_label = ctk.CTkLabel(self, text="Author")
        self.author_label.pack(fill=tk.X, padx=5, pady=5)

        self.author_entry = ctk.CTkEntry(self)
        self.author_entry.pack(fill=tk.X, padx=5, pady=5)
        self.author_entry.insert(0, self.item_data['author'])

        self.language_label = ctk.CTkLabel(self, text="Language")
        self.language_label.pack(fill=tk.X, padx=5, pady=5)

        self.language_entry = ctk.CTkEntry(self)
        self.language_entry.pack(fill=tk.X, padx=5, pady=5)
        self.language_entry.insert(0, self.item_data['language'])

        self.keywords_label = ctk.CTkLabel(self, text="Keywords")
        self.keywords_label.pack(fill=tk.X, padx=5, pady=5)

        self.keywords_entry = ctk.CTkEntry(self)
        self.keywords_entry.pack(fill=tk.X, padx=5, pady=5)
        self.keywords_entry.insert(0, self.item_data['keywords'])

        self.create_button = ctk.CTkButton(
            self, text="Update Article", command=self.update_article_item)
        self.create_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def update_book_item(self):
        title = self.title_entry.get()
        release_year = self.release_year_entry.get()
        author = self.author_entry.get()
        self.controller.update_book_item(
            self.item_data['id_item'], title, release_year, author)
        self.parent.refresh_items(type_item=self.item_type)

        self.destroy()

    def update_magazine_item(self):
        title = self.title_entry.get()
        release_year = self.release_year_entry.get()
        publisher = self.publisher_entry.get()
        pages_count = self.pages_count_entry.get()
        language = self.language_entry.get()
        genre = self.genre_entry.get()
        self.controller.update_magazine_item(
            item_id=self.item_data['id_item'],
            title=title,
            release_year=release_year,
            publisher=publisher,
            pages_count=pages_count,
            language=language,
            genre=genre
        )
        self.parent.refresh_items(type_item=self.item_type)

        self.destroy()

    def update_article_item(self):
        title = self.title_entry.get()
        release_year = self.release_year_entry.get()
        abstract = self.abstract_entry.get()
        word_count = self.word_count_entry.get()
        author = self.author_entry.get()
        language = self.language_entry.get()
        keywords = self.keywords_entry.get()
        self.controller.update_article_item(
            item_id=self.item_data['id_item'],
            title=title,
            release_year=release_year,
            abstract=abstract,
            word_count=word_count,
            author=author,
            language=language,
            keywords=keywords
        )
        self.parent.refresh_items(type_item=self.item_type)

        self.destroy()
