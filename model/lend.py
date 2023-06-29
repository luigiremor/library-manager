
class Lend():

    def __init__(self, lend_date, return_date, status, item, student):
        self.lend_date = lend_date
        self.return_date = return_date
        self.status = status
        self.item = item
        self.student = student

    def get_details(self):
        return f"Lend date: {self.lend_date}\nReturn date: {self.return_date}\nStatus: {self.status}\nItem: {self.item}\nStudent: {self.student}"
