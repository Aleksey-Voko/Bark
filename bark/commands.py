import sys
from abc import abstractmethod
from datetime import datetime

import requests

from database import DatabaseManager

db = DatabaseManager('bookmarks.db')


class Command:
    @abstractmethod
    def execute(self, data):
        pass


class CreateBookmarksTableCommand(Command):
    def execute(self, data=None):
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })


class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Закладка добавлена!'


class ListBookmarksCommand(Command):
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self, data=None):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand(Command):
    def execute(self, data):
        db.delete('bookmarks', {'id': data})
        return 'Закладка удалена!'


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()


class ImportGitHubStarsCommand(Command):
    @staticmethod
    def _extract_bookmark_info(repo):
        return {
            'title': repo['name'],
            'url': repo['html_url'],
            'notes': repo['description'],
        }

    def execute(self, data):
        bookmarks_imported = 0
        github_username = data['github_username']

        next_page_of_results = (
            f'https://api.github.com/users/{github_username}/starred'
        )

        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={'Accept': 'application/vnd.github.v3.star + json'},
            )

            next_page_of_results = (
                stars_response.links.get('next', {}).get('url')
            )

            for repo_info in stars_response.json():
                repo = repo_info['repo']
                if data['preserve_timestamps']:
                    timestamp = datetime.strptime(
                        repo_info['starred_at'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1

                AddBookmarkCommand().execute(
                    self._extract_bookmark_info(repo),
                    timestamp=timestamp,
                )

        return (f'Импортировано {bookmarks_imported} закладок, '
                'помеченных звездами!')
