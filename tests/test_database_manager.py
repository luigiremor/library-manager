import unittest
from database.database_manager import DatabaseManager
from model.article import Article
from model.book import Book
from model.librarian import Librarian
from model.magazine import Magazine
from model.student import Student

from authenticators.authenticator import Authenticator


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseManager('test_library.db')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.db.create_tables()
        self.student = Student(name='Luigi', email='luigi@gmail.com',
                               cpf='12345678910', tel='123456789', registration='123456789')
        self.student2 = Student(
            name='Mario', email='mario@gmail.com', cpf='12345678911', tel='123456789', registration='123456788')
        self.book = Book(title='The Lord of the Rings',
                         author='J. R. R. Tolkien', is_lend=False, release_year=1954)
        self.book2 = Book(title='The Hobbit', author='J. R. R. Tolkien',
                          is_lend=False, release_year='1937')
        self.article = Article(title='The Power of Habit', release_year=2012, is_lend=False, abstract='Lalalalala',
                               word_count='371', author='Luigi', language='English', keywords='Habit, Self-help, Psychology')
        self.magazine = Magazine(
            title='Superinteressante', release_year=2019, is_lend=False, publisher='Abril', pages_count='100', language='Portuguese', genre='Science')
        self.librarian = Librarian(name='Luigi', email='luigi@gmail.com')
        self.password = '123456'

    def tearDown(self):
        self.db.drop_tables()

    def test_librarian_password_authentication(self):
        self.db.create_librarian(
            self.librarian.name, self.librarian.email, self.password)
        stored_password = self.db.get_librarian_password(self.librarian.email)
        self.assertTrue(Authenticator.verify_password(
            stored_password, self.password))
        self.assertFalse(Authenticator.verify_password(
            stored_password, 'wrong_password'))

    def test_create_and_retrieve_librarian(self):
        self.db.create_librarian(
            self.librarian.name, self.librarian.email, self.password)
        librarian_db = self.db.get_librarian_by_email(self.librarian.email)
        self.assertEqual(self.librarian.name, librarian_db['name'])
        self.assertEqual(self.librarian.email, librarian_db['email'])

    def test_create_and_retrieve_student(self):
        self.db.create_student(self.student.name, self.student.email,
                               self.student.cpf, self.student.tel, self.student.registration)
        student_db = self.db.get_student_by_registration(
            self.student.registration)
        self.assertEqual(self.student.name, student_db['name'])
        self.assertEqual(self.student.email, student_db['email'])
        self.assertEqual(self.student.cpf, student_db['cpf'])
        self.assertEqual(self.student.tel, student_db['tel'])
        self.assertEqual(self.student.registration, student_db['registration'])

    def test_get_all_students(self):
        self.db.create_student(self.student.name, self.student.email,
                               self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_student('Mario', 'mario@gmail.com',
                               '12345678911', '123456789', '123456788')
        students_db = self.db.get_all_students()
        self.assertEqual(2, len(students_db))

    def test_create_and_retrieve_book(self):
        self.db.create_book_item(
            self.book.title, self.book.release_year, self.book.author)
        book_db = self.db.get_book_item_by_id(1)
        self.assertEqual(self.book.title, book_db['title'])
        self.assertEqual(self.book.author, book_db['author'])
        self.assertEqual(self.book.release_year, book_db['release_year'])
        self.assertEqual(self.book.is_lend, book_db['is_lend'])

    def test_lend_book_to_student(self):
        self.db.create_student(self.student.name, self.student.email,
                               self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book_item(
            self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item_by_id(1)
        self.db.lend_item(book_db['id'], self.student.registration)
        book_db = self.db.get_book_item_by_id(1)
        self.assertTrue(book_db['is_lend'])

    def test_return_item_from_student(self):
        self.db.create_student(self.student.name, self.student.email,
                               self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book_item(
            self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item_by_id(1)
        self.db.lend_item(book_db['id'], self.student.registration)
        self.db.return_item(book_db['id'])
        book_db = self.db.get_book_item_by_id(1)
        self.assertFalse(book_db['is_lend'])

    def test_get_student_who_borrowed_book(self):
        self.db.create_student(self.student.name, self.student.email,
                               self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_book_item(
            self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item_by_id(1)
        self.db.lend_item(book_db['id'], self.student.registration)
        student_db = self.db.get_student_who_borrowed_item(book_db['id'])
        book_db = self.db.get_book_item_by_id(1)
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
        article_db = self.db.get_article_item_by_id(1)
        self.assertEqual(self.article.title, article_db['title'])
        self.assertEqual(self.article.release_year, article_db['release_year'])
        self.assertEqual(int(self.article.word_count),
                         article_db['word_count'])
        self.assertEqual(self.article.abstract, article_db['abstract'])
        self.assertEqual(self.article.author, article_db['author'])
        self.assertEqual(self.article.language, article_db['language'])
        self.assertEqual(self.article.keywords, article_db['keywords'])
        self.assertEqual(self.article.is_lend, article_db['is_lend'])

    def test_lend_article_to_student(self):
        self.db.create_student(self.student.name, self.student.email,
                               self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_article_item(
            release_year=self.article.release_year,
            title=self.article.title,
            abstract=self.article.abstract,
            word_count=self.article.word_count,
            author=self.article.author,
            language=self.article.language,
            keywords=self.article.keywords)
        article_db = self.db.get_article_item_by_id(1)
        self.db.lend_item(article_db['id'], self.student.registration)
        article_db = self.db.get_article_item_by_id(1)
        self.assertTrue(article_db['is_lend'])

    def test_return_article_from_student(self):
        self.db.create_student(self.student.name, self.student.email,
                               self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_article_item(
            release_year=self.article.release_year,
            title=self.article.title,
            abstract=self.article.abstract,
            word_count=self.article.word_count,
            author=self.article.author,
            language=self.article.language,
            keywords=self.article.keywords)
        article_db = self.db.get_article_item_by_id(1)
        self.db.lend_item(article_db['id'], self.student.registration)
        self.db.return_item(article_db['id'])
        article_db = self.db.get_article_item_by_id(1)
        self.assertFalse(article_db['is_lend'])

    def test_create_and_get_magazine(self):
        self.db.create_magazine_item(title=self.magazine.title,
                                     release_year=self.magazine.release_year,
                                     publisher=self.magazine.publisher,
                                     pages_count=self.magazine.pages_count,
                                     genre=self.magazine.genre,
                                     language=self.magazine.language)
        magazine_db = self.db.get_magazine_item_by_id(1)
        self.assertEqual(self.magazine.title, magazine_db['title'])
        self.assertEqual(self.magazine.release_year,
                         magazine_db['release_year'])
        self.assertEqual(int(self.magazine.pages_count),
                         magazine_db['pages_count'])
        self.assertEqual(self.magazine.publisher, magazine_db['publisher'])
        self.assertEqual(self.magazine.genre, magazine_db['genre'])
        self.assertEqual(self.magazine.language, magazine_db['language'])
        self.assertEqual(self.magazine.is_lend, magazine_db['is_lend'])

    def test_get_all_students_who_borrowed_item(self):
        self.db.create_student(self.student.name, self.student.email,
                               self.student.cpf, self.student.tel, self.student.registration)
        self.db.create_student(self.student2.name, self.student2.email,
                               self.student2.cpf, self.student2.tel, self.student2.registration)
        self.db.create_book_item(
            self.book.title, self.book.author, self.book.release_year)
        self.db.create_book_item(
            self.book2.title, self.book2.author, self.book2.release_year)
        book_db = self.db.get_book_item_by_id(1)
        book_db2 = self.db.get_book_item_by_id(2)
        self.db.lend_item(book_db['id'], self.student.registration)
        self.db.lend_item(book_db2['id'], self.student2.registration)
        students_db = self.db.get_all_students_who_borrowed_item()
        self.assertEqual(2, len(students_db))

    def test_update_book_item(self):
        self.db.create_book_item(
            self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item_by_id(1)
        self.db.update_book_item(
            book_db['id'], title='Novo titulo', author='Novo autor', release_year=2018)
        book_db = self.db.get_book_item_by_id(1)
        self.assertEqual('Novo titulo', book_db['title'])
        self.assertEqual('Novo autor', book_db['author'])
        self.assertEqual(2018, book_db['release_year'])

    def test_update_article_item(self):
        self.db.create_article_item(
            release_year=self.article.release_year,
            title=self.article.title,
            abstract=self.article.abstract,
            word_count=self.article.word_count,
            author=self.article.author,
            language=self.article.language,
            keywords=self.article.keywords)
        article_db = self.db.get_article_item_by_id(1)
        self.db.update_article_item(article_db['id'], title='Novo titulo', release_year=2018, abstract='Novo abstract',
                                    word_count=100, author='Novo autor', language='Novo idioma', keywords='Novas palavras')
        article_db = self.db.get_article_item_by_id(1)
        self.assertEqual(2018, article_db['release_year'])
        self.assertEqual('Novo titulo', article_db['title'])
        self.assertEqual('Novo abstract', article_db['abstract'])
        self.assertEqual(100, article_db['word_count'])
        self.assertEqual('Novo autor', article_db['author'])
        self.assertEqual('Novo idioma', article_db['language'])
        self.assertEqual('Novas palavras', article_db['keywords'])

    def test_update_magazine_item(self):
        self.db.create_magazine_item(release_year=self.magazine.release_year,
                                     title=self.magazine.title,
                                     publisher=self.magazine.publisher,
                                     pages_count=self.magazine.pages_count,
                                     genre=self.magazine.genre,
                                     language=self.magazine.language)
        magazine_db = self.db.get_magazine_item_by_id(1)
        self.db.update_magazine_item(magazine_db['id'], title='Novo titulo', release_year=2018,
                                     publisher='Nova editora', pages_count=100, genre='Novo genero', language='Novo idioma')
        magazine_db = self.db.get_magazine_item_by_id(1)
        self.assertEqual(2018, magazine_db['release_year'])
        self.assertEqual('Novo titulo', magazine_db['title'])
        self.assertEqual('Nova editora', magazine_db['publisher'])
        self.assertEqual(100, magazine_db['pages_count'])
        self.assertEqual('Novo genero', magazine_db['genre'])
        self.assertEqual('Novo idioma', magazine_db['language'])

    def test_delete_item(self):
        self.db.create_book_item(
            self.book.title, self.book.author, self.book.release_year)
        book_db = self.db.get_book_item_by_id(1)
        self.db.delete_item(book_db['id'], 'book')
        book_db = self.db.get_book_item_by_id(1)
        self.assertIsNone(book_db)

    def test_get_all_items(self):
        self.db.create_book_item(
            self.book.title, self.book.author, self.book.release_year)
        self.db.create_article_item(
            release_year=self.article.release_year,
            title=self.article.title,
            abstract=self.article.abstract,
            word_count=self.article.word_count,
            author=self.article.author,
            language=self.article.language,
            keywords=self.article.keywords)
        self.db.create_magazine_item(title=self.magazine.title,
                                     release_year=self.magazine.release_year,
                                     publisher=self.magazine.publisher,
                                     pages_count=self.magazine.pages_count,
                                     genre=self.magazine.genre,
                                     language=self.magazine.language)
        items_db = self.db.get_all_items()
        self.assertEqual(3, len(items_db))

    def test_get_all_items_by_type(self):
        self.db.create_book_item(
            self.book.title, self.book.author, self.book.release_year)
        self.db.create_article_item(
            release_year=self.article.release_year,
            title=self.article.title,
            abstract=self.article.abstract,
            word_count=self.article.word_count,
            author=self.article.author,
            language=self.article.language,
            keywords=self.article.keywords)
        self.db.create_magazine_item(title=self.magazine.title,
                                     release_year=self.magazine.release_year,
                                     publisher=self.magazine.publisher,
                                     pages_count=self.magazine.pages_count,
                                     genre=self.magazine.genre,
                                     language=self.magazine.language)
        items_db = self.db.get_all_items_by_type('book')
        self.assertEqual(1, len(items_db))
        items_db = self.db.get_all_items_by_type('article')
        self.assertEqual(1, len(items_db))
        items_db = self.db.get_all_items_by_type('magazine')
        self.assertEqual(1, len(items_db))

    def test_update_student(self):
        self.db.create_student(name=self.student.name, email=self.student.email, cpf=self.student.cpf, tel=self.student.tel,
                               registration=self.student.registration)
        student_db = self.db.get_student_by_registration(
            self.student.registration)
        self.db.update_student(student_id=student_db['id'], name='Novo nome', email='Novo email', cpf='12345678999',
                               tel='Novo telefone', registration='12345678999')

        student_db = self.db.get_student_by_registration('12345678999')
        self.assertEqual('Novo nome', student_db['name'])
        self.assertEqual('Novo email', student_db['email'])
        self.assertEqual('Novo telefone', student_db['tel'])
        self.assertEqual('12345678999', student_db['registration'])

    def test_delete_student_item(self):
        self.db.create_student(name=self.student.name, email=self.student.email, cpf=self.student.cpf, tel=self.student.tel,
                               registration=self.student.registration)
        student_db = self.db.get_student_by_registration(
            self.student.registration)
        self.db.delete_student_by_registration(self.student.registration)
        student_db = self.db.get_student_by_registration(
            self.student.registration)
        self.assertIsNone(student_db)


if __name__ == '__main__':
    unittest.main()
