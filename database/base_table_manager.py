import sqlite3


class BaseTableManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

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
