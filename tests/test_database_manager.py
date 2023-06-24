import unittest
from database.database_manager import DatabaseManager
from model.librarian import Librarian
from model.student import Student


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This method will be called once before running all tests
        # Create a new database for testing
        cls.db = DatabaseManager('test_library.db')

    @classmethod
    def tearDownClass(cls):
        # This method will be called once after running all tests
        # Delete the test database if needed
        # drop all the db tables
        cls.db.drop_tables()

    def setUp(self):
        # This method will be called before running each test
        # Create tables
        self.db.create_tables()

    def tearDown(self):
        # This method will be called after running each test
        # Clean the database, you might drop tables or delete the db file
        pass

    def test_authentication_librarian(self):
        # Create a new librarian
        librarian = Librarian('Luigi', 'luigi@gmail.com')
        password = '123456'
        self.db.create_librarian(librarian.name, librarian.email, password)

        # Verify the password
        stored_password = self.db.get_librarian_password(librarian.email)
        self.assertTrue(self.db.verify_password(stored_password, password))

        # Verify a wrong password
        self.assertFalse(self.db.verify_password(
            stored_password, 'wrong_password'))

    def test_create_and_get_librarian(self):

        # Create a new librarian
        librarian = Librarian('Luigi', 'luigi@gmail.com')
        password = '123456'
        self.db.create_librarian(librarian.name, librarian.email, password)

        # Verify the librarian
        librarian_db = self.db.get_librarian(librarian.email)

        self.assertEqual(librarian.name, librarian_db[1])
        self.assertEqual(librarian.email, librarian_db[2])

    def test_create_and_get_student(self):
        # Create a new student
        student = Student('Luigi', 'luigi@gmail.com',
                          '12345678910', '123456789', '123456789')
        self.db.create_student(student.name, student.email,
                               student.cpf, student.tel, student.registration)

        # Verify the student
        student_db = self.db.get_student(student.registration)

        self.assertEqual(student.name, student_db[1])
        self.assertEqual(student.email, student_db[2])
        self.assertEqual(student.cpf, student_db[3])
        self.assertEqual(student.tel, student_db[4])
        self.assertEqual(student.registration, student_db[5])


# If the script is run directly, run the tests
if __name__ == '__main__':
    unittest.main()
