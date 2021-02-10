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
