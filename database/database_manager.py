from datetime import datetime, timedelta
from tkinter import messagebox
from authenticators.authenticator import Authenticator
from database.base_table_manager import BaseTableManager
from datetime import datetime


class DatabaseManager(BaseTableManager):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.create_tables()

    # Tables

    def create_tables(self):
        # Create tables for Library, Person, Item, Lend etc.
        self.create_table_librarian()
        self.create_table_student()
        self.create_table_item()
        self.create_table_book_item()
        self.create_table_article_item()
        self.create_table_magazine_item()
        # Add other item types like self.create_table_magazine_item() or self.create_table_article_item()
        self.create_table_lend()

    def create_table_librarian(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS librarians (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def create_table_student(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                tel TEXT NOT NULL,
                registration TEXT UNIQUE NOT NULL,
                fine_delay REAL NOT NULL DEFAULT 0
            )
        """)
        self.conn.commit()

    def create_table_item(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                release_year INTEGER NOT NULL,
                is_lend INTEGER NOT NULL DEFAULT 0,
                id_student_lent INTEGER,
                FOREIGN KEY (id_student_lent) REFERENCES students (id)
            )
        """)
        self.conn.commit()

    def create_table_book_item(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_items (
                id INTEGER PRIMARY KEY,
                author TEXT NOT NULL,
                id_item INTEGER NOT NULL,
                FOREIGN KEY (id_item) REFERENCES items (id)
            )
        """)
        self.conn.commit()

    def create_table_article_item(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS article_items (
                id INTEGER PRIMARY KEY,
                abstract TEXT NOT NULL,
                word_count INTEGER NOT NULL,
                author TEXT NOT NULL,
                language TEXT NOT NULL,
                keywords TEXT NOT NULL,
                id_item INTEGER NOT NULL,
                FOREIGN KEY (id_item) REFERENCES items (id)
            )
        """)
        self.conn.commit()

    def create_table_magazine_item(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazine_items (
                id INTEGER PRIMARY KEY,
                publisher TEXT NOT NULL,
                pages_count INTEGER NOT NULL,
                language TEXT NOT NULL,
                genre TEXT NOT NULL,
                id_item INTEGER NOT NULL,
                FOREIGN KEY (id_item) REFERENCES items (id)
            )
        """)
        self.conn.commit()

    def create_table_lend(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lends (
                id INTEGER PRIMARY KEY,
                lend_date TEXT NOT NULL,
                return_date TEXT NOT NULL,
                status TEXT NOT NULL,
                id_student INTEGER NOT NULL,
                id_item INTEGER NOT NULL,
                FOREIGN KEY (id_student) REFERENCES students (id),
                FOREIGN KEY (id_item) REFERENCES items (id)
            )
        """)
        self.conn.commit()

    # CRUD

    def login(self, email, password):
        if not self.is_email_registered(email):
            return False

        hashed_password = self.get_librarian_password(email)
        return Authenticator.verify_password(hashed_password, password)

    def get_librarian_password(self, email):
        password = self.select_one('librarians', 'email', email)['password']
        return password

    def is_email_registered(self, email):
        return self.select_one('librarians', 'email', email) is not None

    def create_librarian(self, name, email, password):
        if self.is_email_registered(email):
            return False

        hashed_password = Authenticator.hash_password(password)
        self.insert('librarians', ['name', 'email', 'password'], [
                    name, email, hashed_password])
        return True

    def create_student(self, name, email, cpf, tel, registration):
        self.insert('students', ['name', 'email', 'cpf', 'tel', 'registration'], [
                    name, email, cpf, tel, registration])
        is_student_created = self.select_one(
            'students', 'registration', registration) is not None
        if is_student_created:
            return True
        return False

    def get_librarian_by_email(self, email):
        return self.select_one('librarians', 'email', email)

    def get_student_by_registration(self, registration):
        return self.select_one('students', 'registration', registration)

    def get_all_students(self):
        return self.select_all('students')

    def create_book_item(self, title, release_year, author):
        self.insert('items', ['title', 'release_year'], [title, release_year])
        last_inserted_id = self.cursor.lastrowid
        self.insert('book_items', ['author', 'id_item'], [
                    author, last_inserted_id])

        return last_inserted_id

    def create_article_item(self, title, release_year, abstract, word_count, author, language, keywords):
        self.insert('items', ['title', 'release_year'], [title, release_year])
        last_inserted_id = self.cursor.lastrowid
        self.insert('article_items', ['abstract', 'word_count', 'author', 'language', 'keywords', 'id_item'], [
                    abstract, word_count, author, language, keywords, last_inserted_id])

        return last_inserted_id

    def create_magazine_item(self, title, release_year, publisher, pages_count, language, genre):
        self.insert('items', ['title', 'release_year'], [title, release_year])
        last_inserted_id = self.cursor.lastrowid
        self.insert('magazine_items', ['publisher', 'pages_count', 'language', 'genre', 'id_item'], [
                    publisher, pages_count, language, genre, last_inserted_id])

        return last_inserted_id

    def get_all_items(self):
        return self.select_all('items')

    def get_all_items_by_type(self, item_type):
        self.cursor.execute(f"""
            SELECT items.*, {item_type}_items.*
            FROM items
            JOIN {item_type}_items ON items.id = {item_type}_items.id_item
        """)
        result = self.cursor.fetchall()

        if result:
            columns = [column[0] for column in self.cursor.description]
            return [dict(zip(columns, row)) for row in result]

        return None

    def get_complete_item_details_by_id(self, item_id, item_type):
        self.cursor.execute(f"""
            SELECT items.*, {item_type}_items.*
            FROM items
            JOIN {item_type}_items ON items.id = {item_type}_items.id_item
            WHERE items.id = ?
        """, (item_id,))
        result = self.cursor.fetchone()

        if result:
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, result))

        return None

    def get_book_item_by_id(self, item_id):
        self.cursor.execute("""
            SELECT items.*, book_items.author 
            FROM items
            JOIN book_items ON items.id = book_items.id_item
            WHERE items.id = ?
        """, (item_id,))
        result = self.cursor.fetchone()

        if result:
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, result))

        return None

    def get_magazine_item_by_id(self, item_id):
        self.cursor.execute("""
            SELECT items.*, magazine_items.*
            FROM items
            JOIN magazine_items ON items.id = magazine_items.id_item
            WHERE items.id = ?
        """, (item_id,))
        result = self.cursor.fetchone()

        if result:
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, result))

        return None

    def get_article_item_by_id(self, item_id):
        self.cursor.execute("""
            SELECT items.*, article_items.*
            FROM items
            JOIN article_items ON items.id = article_items.id_item
            WHERE items.id = ?
        """, (item_id,))
        result = self.cursor.fetchone()

        if result:
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, result))

        return None

    def update_book_item(self, item_id, title, author, release_year):
        self.cursor.execute("""
            UPDATE items
            SET title = ?, release_year = ?
            WHERE id = ?
        """, (title, release_year, item_id))

        self.cursor.execute("""
            UPDATE book_items
            SET author = ?
            WHERE id_item = ?
        """, (author, item_id))

        self.conn.commit()

    def update_magazine_item(self, item_id, release_year, title, publisher, pages_count, language, genre):
        self.cursor.execute("""
            UPDATE items
            SET title = ?, release_year = ?
            WHERE id = ?
        """, (title, release_year, item_id))

        self.cursor.execute("""
            UPDATE magazine_items
            SET publisher = ?, pages_count = ?, language = ?, genre = ?
            WHERE id_item = ?
        """, (publisher, pages_count, language, genre, item_id))

        self.conn.commit()

    def update_article_item(self, item_id, title, release_year, abstract, word_count, author, language, keywords):
        self.cursor.execute("""
            UPDATE items
            SET title = ?, release_year = ?
            WHERE id = ?
        """, (title, release_year, item_id))

        self.cursor.execute("""
            UPDATE article_items
            SET abstract = ?, word_count = ?, author = ?, language = ?, keywords = ?
            WHERE id_item = ?
        """, (abstract, word_count, author, language, keywords, item_id))

        self.conn.commit()

    def delete_item(self, item_id, item_type):
        self.cursor.execute("""
            DELETE FROM items
            WHERE id = ?
        """, (item_id,))

        self.cursor.execute(f"""
            DELETE FROM {item_type}_items
            WHERE id_item = ?
        """, (item_id,))

        self.conn.commit()

    def lend_item(self, item_id, student_id):
        self.cursor.execute("""
            UPDATE items
            SET is_lend = 1, id_student_lent = ?
            WHERE id = ?
        """, (student_id, item_id))

        lend_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return_date = (datetime.now() + timedelta(days=7)
                       ).strftime("%Y-%m-%d %H:%M:%S")
        status = 'lent'
        self.insert('lends', ['lend_date', 'return_date', 'status', 'id_student', 'id_item'],
                    [lend_date, return_date, status, student_id, item_id])

        self.conn.commit()

    def get_all_lends(self):
        return self.select_all('lends')

    def return_item(self, lend_id, fine_per_day=1):
        # Get the return date and student id from lends table
        self.cursor.execute("""
            SELECT return_date, id_student FROM lends WHERE id = ?
        """, (lend_id,))
        result = self.cursor.fetchone()

        if result is None:
            raise ValueError("No such lend exists")

        return_date_str, student_id = result
        return_date = datetime.strptime(return_date_str, "%Y-%m-%d %H:%M:%S")

        # Calculate fine if today's date is greater than return date
        today = datetime.now()
        if today > return_date:
            days_overdue = (today - return_date).days
            fine = days_overdue * fine_per_day

            # Update the fine_delay for the student in students table
            self.cursor.execute("""
                UPDATE students
                SET fine_delay = fine_delay + ?
                WHERE id = ?
            """, (fine, student_id))
            self.conn.commit()

        # Update the items table and delete the record from lends table
        self.cursor.execute("""
            UPDATE items
            SET is_lend = 0, id_student_lent = NULL
            WHERE id = (
                SELECT id_item FROM lends WHERE id = ?
            )
        """, (lend_id,))
        self.conn.commit()

        self.cursor.execute("""
            DELETE FROM lends
            WHERE id = ?
        """, (lend_id,))
        self.conn.commit()

    def get_student_who_borrowed_item(self, item_id):
        self.cursor.execute("""
            SELECT students.* 
            FROM items
            JOIN students ON items.id_student_lent = students.registration
            WHERE items.id = ?
        """, (item_id,))
        result = self.cursor.fetchone()

        if result:
            columns = [column[0] for column in self.cursor.description]
            student = dict(zip(columns, result))
            return student

        return None

    def get_all_students_who_borrowed_item(self):
        self.cursor.execute("""
            SELECT students.* 
            FROM items
            JOIN students ON items.id_student_lent = students.registration
            GROUP BY students.registration
        """)
        result = self.cursor.fetchall()

        if result:
            columns = [column[0] for column in self.cursor.description]
            students = []
            for row in result:
                students.append(dict(zip(columns, row)))
            return students

        return None

    def get_all_lendings(self):
        self.cursor.execute("""
            SELECT lends.*, items.title, students.registration, students.name
            FROM lends
            JOIN items ON lends.id_item = items.id
            JOIN students ON lends.id_student = students.id
        """)
        result = self.cursor.fetchall()

        if result:
            columns = [column[0] for column in self.cursor.description]
            lendings = []
            for row in result:
                lendings.append(dict(zip(columns, row)))
            return lendings

        return None

    def update_student(self, student_id, name, email, cpf, tel, registration):
        self.cursor.execute("""
            UPDATE students
            SET name = ?, email = ?, cpf = ?, tel = ?, registration = ?
            WHERE id = ?
        """, (name, email, cpf, tel, registration, student_id))

        self.conn.commit()

    def delete_student_by_registration(self, registration):
        self.cursor.execute("""
            DELETE FROM students
            WHERE registration = ?
        """, (registration,))

        self.conn.commit()

    def pay_student_debt(self, student_id, amount):
        self.cursor.execute("""
            SELECT fine_delay
            FROM students
            WHERE id = ?
        """, (student_id,))
        result = self.cursor.fetchone()
        if result:
            fine_delay = result[0]
            if amount > fine_delay:
                raise ValueError("Amount is greater than the fine delay")
            self.cursor.execute("""
                UPDATE students
                SET fine_delay = fine_delay - ?
                WHERE id = ?
            """, (amount, student_id))
            self.conn.commit()
        else:
            raise ValueError("Student not found")

    # Implement similar methods for all operations (insert, update, delete, select) on each table
    # For example, insert_item, delete_item, select_item, update_item etc.

    def close_connection(self):
        self.conn.close()

    def drop_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS librarians")
        self.cursor.execute("DROP TABLE IF EXISTS students")
        self.cursor.execute("DROP TABLE IF EXISTS items")
        self.cursor.execute("DROP TABLE IF EXISTS book_items")
        self.cursor.execute("DROP TABLE IF EXISTS article_items")
        self.cursor.execute("DROP TABLE IF EXISTS magazine_items")
        self.cursor.execute("DROP TABLE IF EXISTS lends")
        self.conn.commit()
