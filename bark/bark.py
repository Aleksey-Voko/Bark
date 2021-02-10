from collections import OrderedDict

from bark import commands


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


def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()

    options = OrderedDict({
        'A': Option('Добавить закладку', commands.AddBookmarkCommand()),
        'B': Option('Показать список закладок по дате',
                    commands.ListBookmarksCommand()),
        'T': Option('Показать список закладок по заголовку',
                    commands.ListBookmarksCommand(order_by='title')),
        'D': Option('Удалить закладку', commands.DeleteBookmarkCommand()),
        'Q': Option('Выйти', commands.QuitCommand()),
    })
    print_options(options)
