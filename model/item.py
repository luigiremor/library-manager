from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, title, release_year=None, is_lend=False, is_reserved=False):
        self.title = title
        self.release_year = release_year
        self.is_lend = is_lend
        self.is_reserved = is_reserved

    @abstractmethod
    def get_details(self):
        pass
