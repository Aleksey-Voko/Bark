import os
from collections import OrderedDict
from pprint import pprint

import commands

ACTION_OPTION = 'Выберите вариант действия'
INVALID_OPTION = 'Недопустимый вариант'
ADD_BOOKMARK = 'Добавить закладку'
BOOKMARKS_BY_DATE = 'Показать список закладок по дате'
BOOKMARKS_BY_TITLE = 'Показать список закладок по заголовку'
DELETE_BOOKMARK = 'Удалить закладку'
QUIT = 'Выйти'


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data)
        pprint(message)

    def __str__(self):
        return self.name


def print_options(opt):
    for shortcut, option in opt.items():
        print(f'({shortcut}) {option}')
    print()


def option_choice_is_valid(choice, opt):
    return choice in opt or choice.upper() in opt


def get_option_choice(opt):
    choice = input(f'{ACTION_OPTION}: ')

    while not option_choice_is_valid(choice, opt):
        print(INVALID_OPTION)
        choice = input(f'{ACTION_OPTION}: ')

    return opt[choice.upper()]


def get_github_import_options():
    return {
        'github_username': get_user_input('Пользовательское имя GitHub'),
        'preserve_timestamps':
            get_user_input(
                'Сохранить метки времени [Д/н]',
                required=False
            ) in {'Д', 'д', None},
    }


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data():
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False),
    }


def get_bookmark_id_for_deletion():
    return get_user_input('Enter a bookmark ID to delete')


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def loop():
    options = OrderedDict({
        'A': Option(ADD_BOOKMARK, commands.AddBookmarkCommand(),
                    prep_call=get_new_bookmark_data),
        'B': Option(BOOKMARKS_BY_DATE, commands.ListBookmarksCommand()),
        'T': Option(BOOKMARKS_BY_TITLE,
                    commands.ListBookmarksCommand(order_by='title')),
        'D': Option(DELETE_BOOKMARK, commands.DeleteBookmarkCommand(),
                    prep_call=get_bookmark_id_for_deletion),
        'Q': Option(QUIT, commands.QuitCommand()),
        'G': Option(
            'Импортировать звезды GitHub',
            commands.ImportGitHubStarsCommand(),
            prep_call=get_github_import_options
        ),
    })
    clear_screen()
    print_options(options)

    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()

    _ = input('Нажмите ENTER для возврата в меню')


if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()

    while True:
        loop()
