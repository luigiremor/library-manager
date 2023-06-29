
from model.item import Item


class Article(Item):

    def __init__(self, title, release_year=None, is_lend=False, abstract=None, word_count=None, author=None, language=None, keywords=None):
        super().__init__(title, release_year, is_lend)
        self.abstract = abstract
        self.word_count = word_count
        self.author = author
        self.language = language
        self.keywords = keywords

    def get_details(self):
        return f"Article: {self.title} ({self.release_year})\nAbstract: {self.abstract}\nWord count: {self.word_count}\nAuthor: {self.author}\nLanguage: {self.language}\nKeywords: {self.keywords}"

    def get_abstract(self):
        return self.abstract
