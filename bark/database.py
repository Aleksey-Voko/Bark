import sqlite3


class DatabaseManager:
    def __init__(self, db_filename):
        self.connection = sqlite3.connect(db_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor


if __name__ == '__main__':
    db_manager = DatabaseManager('data_base.db')
