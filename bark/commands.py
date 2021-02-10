import sys
from datetime import datetime

from bark.database import DatabaseManager

db = DatabaseManager('bookmarks.db')


class CreateBookmarksTableCommand:
    @staticmethod
    def execute():
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })


class AddBookmarkCommand:
    @staticmethod
    def execute(data):
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Закладка добавлена!'


class ListBookmarksCommand:
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    @staticmethod
    def execute(data):
        db.delete('bookmarks', {'id': data})
        return 'Закладка удалена!'


class QuitCommand:
    @staticmethod
    def execute():
        sys.exit()
