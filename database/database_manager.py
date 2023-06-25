import binascii
from datetime import datetime, timedelta
import hashlib
import os
import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Create tables for Library, Person, Item, Reservation, Lend etc.
        self.create_table_librarian()
        self.create_table_student()
        self.create_table_item()
        self.create_table_book_item()
        self.create_table_article_item()
        self.create_table_magazine_item()
        # Add other item types like self.create_table_magazine_item() or self.create_table_article_item()
        self.create_table_reservation()
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
                release_year TEXT NOT NULL,
                is_lend INTEGER NOT NULL DEFAULT 0,
                is_reserved INTEGER NOT NULL DEFAULT 0,
                id_student_lent INTEGER,
                id_student_reserved INTEGER,
                FOREIGN KEY (id_student_lent) REFERENCES students (id),
                FOREIGN KEY (id_student_reserved) REFERENCES students (id)
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

    def create_table_reservation(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY,
                reservation_date TEXT NOT NULL,
                status TEXT NOT NULL,
                id_student INTEGER NOT NULL,
                id_item INTEGER NOT NULL,
                FOREIGN KEY (id_student) REFERENCES students (id),
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

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def insert(self, table, fields, values):
        query = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(['?' for _ in values])})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def select_one(self, table, field, value):
        query = f"SELECT * FROM {table} WHERE {field} = ?"
        self.cursor.execute(query, (value,))
        result = self.cursor.fetchone()

        if result:
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, result))

        return None

    def select_all(self, table):
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        if result:
            columns = [column[0] for column in self.cursor.description]
            return [dict(zip(columns, row)) for row in result]

        return None

    def get_librarian_password(self, email):
        password = self.select_one('librarians', 'email', email)['password']
        return password

    def is_email_registered(self, email):
        return self.select_one('librarians', 'email', email) is not None

    def create_librarian(self, name, email, password):
        if self.is_email_registered(email):
            return False

        hashed_password = self.hash_password(password)
        self.insert('librarians', ['name', 'email', 'password'], [
                    name, email, hashed_password])
        return True

    def create_student(self, name, email, cpf, tel, registration):
        self.insert('students', ['name', 'email', 'cpf', 'tel', 'registration'], [
                    name, email, cpf, tel, registration])

    def get_librarian(self, email):
        return self.select_one('librarians', 'email', email)

    def get_student(self, registration):
        return self.select_one('students', 'registration', registration)
    
    def get_all_students(self):
        return self.select_all('students')
    
    def get_book_item(self, item_id):
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

    
    def create_book_item(self, title, author, release_year):
        self.insert('items', ['title', 'release_year'], [title, release_year])
        last_inserted_id = self.cursor.lastrowid
        self.insert('book_items', ['author', 'id_item'], [author, last_inserted_id])
        
        return last_inserted_id
    
    def create_article_item(self, release_year, title, abstract, word_count, author, language, keywords):
        self.insert('items', ['title', 'release_year'], [title, release_year])
        last_inserted_id = self.cursor.lastrowid
        self.insert('article_items', ['abstract', 'word_count', 'author', 'language', 'keywords', 'id_item'], [abstract, word_count, author, language, keywords, last_inserted_id])

        return last_inserted_id

    def create_magazine_item(self, release_year, title, publisher, pages_count, language, genre):
        self.insert('items', ['title', 'release_year'], [title, release_year])
        last_inserted_id = self.cursor.lastrowid
        self.insert('magazine_items', ['publisher', 'pages_count', 'language', 'genre', 'id_item'], [publisher, pages_count, language, genre, last_inserted_id])

        return last_inserted_id

    def get_magazine_item(self, item_id):
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

    def get_article_item(self, item_id):
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

    def reserve_item(self, item_id, student_id):
        self.cursor.execute("""
            UPDATE items
            SET is_reserved = 1, id_student_reserved = ?
            WHERE id = ?
        """, (student_id, item_id))

        reservation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = 'reserved'
        self.insert('reservations', ['reservation_date', 'status', 'id_student', 'id_item'], 
                    [reservation_date, status, student_id, item_id])

        self.conn.commit()

    def lend_item(self, item_id, student_id):
        self.cursor.execute("""
            UPDATE items
            SET is_lend = 1, id_student_lent = ?
            WHERE id = ?
        """, (student_id, item_id))

        lend_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        status = 'lent'
        self.insert('lends', ['lend_date', 'return_date','status', 'id_student', 'id_item'], 
                    [lend_date, return_date, status, student_id, item_id])

        self.conn.commit()

    def get_all_lends(self):
        return self.select_all('lends')

    def cancel_item_reservation(self, item_id):
        self.cursor.execute("""
            UPDATE items
            SET is_reserved = 0, id_student_reserved = NULL
            WHERE id = ?
        """, (item_id,))
        self.conn.commit()

    def return_item(self, item_id):
        self.cursor.execute("""
            UPDATE items
            SET is_lend = 0, id_student_lent = NULL
            WHERE id = ?
        """, (item_id,))
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


    def get_student_who_reserved_item(self, item_id):
        self.cursor.execute("""
            SELECT students.* 
            FROM items
            JOIN students ON items.id_student_reserved = students.registration
            WHERE items.id = ?
        """, (item_id,))
        result = self.cursor.fetchone()

        if result:
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, result))
        
        return None

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
        self.cursor.execute("DROP TABLE IF EXISTS reservations")
        self.conn.commit()
