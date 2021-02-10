from collections import OrderedDict

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
        message = (self.command.execute(data)
                   if data else self.command.execute())
        print(message)

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


if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()

    options = OrderedDict({
        'A': Option(ADD_BOOKMARK, commands.AddBookmarkCommand()),
        'B': Option(BOOKMARKS_BY_DATE, commands.ListBookmarksCommand()),
        'T': Option(BOOKMARKS_BY_TITLE,
                    commands.ListBookmarksCommand(order_by='title')),
        'D': Option(DELETE_BOOKMARK, commands.DeleteBookmarkCommand()),
        'Q': Option(QUIT, commands.QuitCommand()),
    })
    print_options(options)

    chosen_option = get_option_choice(options)
    chosen_option.choose()
