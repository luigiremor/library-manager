import unittest
from database.database_manager import DatabaseManager
from model.book import Book
from model.librarian import Librarian
from model.student import Student


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This method will be called once before running all tests
        cls.db = DatabaseManager('test_library.db')

    @classmethod
    def tearDownClass(cls):
        # This method will be called once after running all tests
        pass

    def setUp(self):
        # This method will be called before running each test
        self.db.create_tables()
        # Initialize objects
        self.student = Student('Luigi', 'luigi@gmail.com', '12345678910', '123456789', '123456789')
        self.book = Book('The Lord of the Rings', 'J. R. R. Tolkien', False, False, '1954')
        self.librarian = Librarian('Luigi', 'luigi@gmail.com')
        self.password = '123456'

    def tearDown(self):
        # This method will be called once after running all tests
        self.db.drop_tables()

    def test_librarian_password_authentication(self):
        self.db.create_librarian(self.librarian.name, self.librarian.email, self.password)
        stored_password = self.db.get_librarian_password(self.librarian.email)
        self.assertTrue(self.db.verify_password(stored_password, self.password))
        self.assertFalse(self.db.verify_password(stored_password, 'wrong_password'))

    def test_create_and_retrieve_librarian(self):
        is_created = self.db.create_librarian(self.librarian.name, self.librarian.email, self.password)
        self.assertTrue(is_created, 'Librarian should be created successfully.')
        librarian_db = self.db.get_librarian(self.librarian.email)
        self.assertEqual(self.librarian.name, librarian_db[1])
        self.assertEqual(self.librarian.email, librarian_db[2])

    def test_create_and_retrieve_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        student_db = self.db.get_student(self.student.registration)
        self.assertEqual(self.student.name, student_db[1])
        self.assertEqual(self.student.email, student_db[2])
        self.assertEqual(self.student.cpf, student_db[3])
        self.assertEqual(self.student.tel, student_db[4])
        self.assertEqual(self.student.registration, student_db[5])

    def test_create_and_retrieve_book(self):
        self.db.create_book(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book(1)
        self.assertEqual(self.book.title, book_db[1])
        self.assertEqual(self.book.author, book_db[2])
        self.assertEqual(self.book.release_year, book_db[3])
        self.assertEqual(self.book.is_lend, book_db[4])
        self.assertEqual(self.book.is_reserved, book_db[5])

    def test_lend_book_to_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book(1)
        self.db.lend_book(book_db[0], self.student.registration)
        book_db = self.db.get_book(1)
        self.assertTrue(book_db[4])

    def test_return_book_from_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book(1)
        self.db.lend_book(book_db[0], self.student.registration)
        self.db.return_book(book_db[0])
        book_db = self.db.get_book(1)
        self.assertFalse(book_db[4])

    def test_reserve_book_to_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book(1)
        self.db.reserve_book(book_db[0], self.student.registration)
        book_db = self.db.get_book(1)
        self.assertTrue(book_db[5])

    def test_cancel_book_reservation_from_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book(self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book(1)
        self.db.reserve_book(book_db[0], self.student.registration)
        self.db.cancel_book_reservation(book_db[0])
        book_db = self.db.get_book(1)
        self.assertFalse(book_db[5])

if __name__ == '__main__':
    unittest.main()
