from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @abstractmethod
    def get_details(self):
        pass
