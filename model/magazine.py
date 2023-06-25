from model.item import Item


class Magazine(Item):

    def __init__(self, title, release_year=None, is_lend=False, is_reserved=False, publisher=None, pages_count=None, language=None, genre=None):
        super().__init__(title, release_year, is_lend, is_reserved)
        self.publisher = publisher
        self.pages_count = pages_count
        self.language = language
        self.genre = genre

    def get_details(self):
        return f"Magazine: {self.title} ({self.release_year})\nPublisher: {self.publisher}\nPages count: {self.pages_count}\nLanguage: {self.language}\nGenre: {self.genre}"