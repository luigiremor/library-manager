from model.person import Person


class Student(Person):

    def __init__(self, name, email, cpf, tel, registration, fine_delay=0):
        super().__init__(name, email)
        self.cpf = cpf
        self.tel = tel
        self.registration = registration
        self.fine_delay = fine_delay

    def get_details(self):
        return f"Student: {self.name}"
