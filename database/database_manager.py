import binascii
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

        # Repeat this for each table you need, adjusting the fields as necessary

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
        return result if result else None

    def select_all(self, table):
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result if result else None

    def get_librarian_password(self, email):
        self.cursor.execute("""
            SELECT password FROM librarians WHERE email = ?
        """, (email,))

        result = self.cursor.fetchone()
        return result[0] if result else None

    def is_email_registered(self, email):
        return self.select_one('librarians', 'email', email) is not None

    def create_librarian(self, name, email, password):
        if self.is_email_registered(email):
            return False

        hashed_password = self.hash_password(password)
        self.insert('librarians', ['name', 'email', 'password'], [
                    name, email, hashed_password])

    def get_librarian(self, email):
        return self.select_one('librarians', 'email', email)

    def create_student(self, name, email, cpf, tel, registration):
        self.insert('students', ['name', 'email', 'cpf', 'tel', 'registration'], [
                    name, email, cpf, tel, registration])

    def get_student(self, registration):
        return self.select_one('students', 'registration', registration)

    # Implement similar methods for all operations (insert, update, delete, select) on each table
    # For example, insert_item, delete_item, select_item, update_item etc.

    def close_connection(self):
        self.conn.close()

    def drop_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS librarians")
        self.cursor.execute("DROP TABLE IF EXISTS students")
        self.conn.commit()
