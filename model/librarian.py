from model.person import Person


class Librarian(Person):
    def __init__(self, name, email):
        super().__init__(name, email)

    def get_details(self):
        return f"Librarian: {self.name}"
