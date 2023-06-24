import unittest
from database.database_manager import DatabaseManager
from model.librarian import Librarian


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
        pass

    def setUp(self):
        # This method will be called before running each test
        # Create tables
        self.db.create_tables()

    def tearDown(self):
        # This method will be called after running each test
        # Clean the database, you might drop tables or delete the db file
        pass

    def test_create_and_get_librarian(self):
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


# If the script is run directly, run the tests
if __name__ == '__main__':
    unittest.main()
