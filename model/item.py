from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, title, release_year=None, is_lend=False):
        self.title = title
        self.release_year = release_year
        self.is_lend = is_lend

    @abstractmethod
    def get_details(self):
        pass
