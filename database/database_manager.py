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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS librarians (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

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

        # Repeat this for each table you need, adjusting the fields as necessary

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

    def get_librarian_password(self, email):
        self.cursor.execute("""
            SELECT password FROM librarians WHERE email = ?
        """, (email,))

        result = self.cursor.fetchone()
        return result[0] if result else None

    def is_email_registered(self, email):
        self.cursor.execute("""
            SELECT email FROM librarians WHERE email = ?
        """, (email,))

        result = self.cursor.fetchone()
        return result[0] if result else None

    def create_librarian(self, name, email, password):
        # check if email already exists
        if self.is_email_registered(email):
            return False

        hashed_password = self.hash_password(password)
        self.cursor.execute("""
            INSERT INTO librarians (name, email, password) VALUES (?, ?, ?)
        """, (name, email, hashed_password))
        self.conn.commit()

    # Implement similar methods for all operations (insert, update, delete, select) on each table
    # For example, insert_item, delete_item, select_item, update_item etc.

    def close_connection(self):
        self.conn.close()
