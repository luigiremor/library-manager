import unittest
from database.database_manager import DatabaseManager
from model.article import Article
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
        self.article = Article('The Power of Habit', '2012', False, False, 'Lalalalala', '371', 'Luigi', 'English', 'Habit, Self-help, Psychology')
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

    def test_create_and_get_article(self):
        self.db.create_article_item(
                                    release_year=self.article.release_year,
                                    title=self.article.title,
                                    abstract=self.article.abstract,
                                    word_count=self.article.word_count,
                                    author=self.article.author,
                                    language=self.article.language,
                                    keywords=self.article.keywords)
        article_db = self.db.get_article_item(1)
        self.assertEqual(self.article.title, article_db['title'])
        self.assertEqual(self.article.release_year, article_db['release_year'])
        self.assertEqual(int(self.article.word_count), article_db['word_count'])
        self.assertEqual(self.article.abstract, article_db['abstract'])
        self.assertEqual(self.article.author, article_db['author'])
        self.assertEqual(self.article.language, article_db['language'])
        self.assertEqual(self.article.keywords, article_db['keywords'])
        self.assertEqual(self.article.is_lend, article_db['is_lend'])
        self.assertEqual(self.article.is_reserved, article_db['is_reserved'])

    def test_lend_article_to_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_article_item(
                                    release_year=self.article.release_year,
                                    title=self.article.title,
                                    abstract=self.article.abstract,
                                    word_count=self.article.word_count,
                                    author=self.article.author,
                                    language=self.article.language,
                                    keywords=self.article.keywords)
        article_db = self.db.get_article_item(1)
        self.db.lend_item(article_db['id'], self.student.registration)
        article_db = self.db.get_article_item(1)
        self.assertTrue(article_db['is_lend'])

    def test_return_article_from_student(self):
        self.db.create_student(self.student.name, self.student.email, self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_article_item(
                                    release_year=self.article.release_year,
                                    title=self.article.title,
                                    abstract=self.article.abstract,
                                    word_count=self.article.word_count,
                                    author=self.article.author,
                                    language=self.article.language,
                                    keywords=self.article.keywords)
        article_db = self.db.get_article_item(1)
        self.db.lend_item(article_db['id'], self.student.registration)
        self.db.return_item(article_db['id'])
        article_db = self.db.get_article_item(1)
        self.assertFalse(article_db['is_lend'])
        

if __name__ == '__main__':
    unittest.main()
