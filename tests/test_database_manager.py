import unittest
from database.database_manager import DatabaseManager
from model.book import Book
from model.librarian import Librarian
from model.student import Student


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseManager('test_library.db')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.db.create_tables()
        self.student = Student('Luigi', 'luigi@gmail.com', '12345678910', '123456789', '123456789')
        self.book = Book('The Lord of the Rings', 'J. R. R. Tolkien', False, False, '1954')
        self.librarian = Librarian('Luigi', 'luigi@gmail.com')
        self.password = '123456'

    def tearDown(self):
        self.db.drop_tables()

    def test_librarian_password_authentication(self):
        self.db.create_librarian(self.librarian.name, self.librarian.email, self.password)
        stored_password = self.db.get_librarian_password(self.librarian.email)
        self.assertTrue(self.db.verify_password(stored_password, self.password))
        self.assertFalse(self.db.verify_password(stored_password, 'wrong_password'))

    def test_create_and_retrieve_librarian(self):
        self.db.create_librarian(self.librarian.name, self.librarian.email, self.password)
        librarian_db = self.db.get_librarian(self.librarian.email)
        self.assertEqual(self.librarian.name, librarian_db['name'])
        self.assertEqual(self.librarian.email, librarian_db['email'])

    def test_create_and_retrieve_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        student_db = self.db.get_student(self.student.registration)
        self.assertEqual(self.student.name, student_db['name'])
        self.assertEqual(self.student.email, student_db['email'])
        self.assertEqual(self.student.cpf, student_db['cpf'])
        self.assertEqual(self.student.tel, student_db['tel'])
        self.assertEqual(self.student.registration, student_db['registration'])

    def test_get_all_students(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_student('Mario', 'mario@gmail.com', '12345678911', '123456789', '123456788')
        students_db = self.db.get_all_students()
        self.assertEqual(2, len(students_db))

    def test_create_and_retrieve_book(self):
        self.db.create_book_item(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item(1)
        self.assertEqual(self.book.title, book_db['title'])
        self.assertEqual(self.book.author, book_db['author'])
        self.assertEqual(self.book.release_year, book_db['release_year'])
        self.assertEqual(self.book.is_lend, book_db['is_lend'])
        self.assertEqual(self.book.is_reserved, book_db['is_reserved'])

    def test_lend_book_to_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book_item(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item(1)
        self.db.lend_item(book_db['id'], self.student.registration)
        book_db = self.db.get_book_item(1)
        self.assertTrue(book_db['is_lend'])

    def test_return_item_from_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book_item(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item(1)
        self.db.lend_item(book_db['id'], self.student.registration)
        self.db.return_item(book_db['id'])
        book_db = self.db.get_book_item(1)
        self.assertFalse(book_db['is_lend'])

    def test_reserve_book_to_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book_item(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item(1)
        self.db.reserve_item(book_db['id'], self.student.registration)
        book_db = self.db.get_book_item(1)
        self.assertTrue(book_db['is_reserved'])

    def test_cancel_book_reservation_from_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book_item(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item(1)
        self.db.reserve_item(book_db['id'], self.student.registration)
        self.db.cancel_item_reservation(book_db['id'])
        book_db = self.db.get_book_item(1)
        self.assertFalse(book_db['is_reserved'])

    def test_get_student_who_borrowed_book(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book_item(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item(1)
        self.db.lend_item(book_db['id'], self.student.registration)
        student_db = self.db.get_student_who_borrowed_item(book_db['id'])
        book_db = self.db.get_book_item(1)
        self.assertEqual(self.student.name, student_db['name'])

    def test_get_student_who_reserved_book(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book_item(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item(1)
        self.db.reserve_item(book_db['id'], self.student.registration)
        student_db = self.db.get_student_who_reserved_item(book_db['id'])
        self.assertEqual(self.student.name, student_db['name'])


if __name__ == '__main__':
    unittest.main()
