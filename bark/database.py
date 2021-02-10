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

    def create_table(self, table_name, columns):
        columns_with_types = [
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items()
        ]

        # noinspection SqlNoDataSourceInspection
        self._execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            '''
        )

    def add(self, table_name, data):
        placeholders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())

        # noinspection SqlNoDataSourceInspection
        self._execute(
            f'''
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            ''',
            column_values,
        )


if __name__ == '__main__':
    db_manager = DatabaseManager('data_base.db')
