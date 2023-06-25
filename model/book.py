from model.item import Item


class Book(Item):
    def __init__(self, title, author, is_lend=False, is_reserved=False, release_year=None):
        super().__init__(title, release_year, is_lend, is_reserved)
        self.author = author

    def get_details(self):
        return f"Book: {self.title} by {self.author}"
