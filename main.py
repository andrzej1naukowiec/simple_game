import abc


#################################################################################
# WYŚWIETLANIE


def wyswietl_old(plansza):
    for linia in plansza:
        for pole in linia:
            print(pole, ", ", end='')
        print()
    print()

def wyswietl(plansza):
    for linia in plansza:
        for pole in linia:
            print(pole, "", end='')
        print()
    print()

def display_hist(game):
    print("historia gry")
    print(str(game['history']))


###################################################################################
# MODEL GRY

PLAYER1 = "X"
PLAYER2 = "O"
EMPTY = "-"
SIZE = 4

def get_position(message, board):
    USER_MIN_VALUE = 1
    USER_MAX_VALUE = SIZE**2
    while True:
        human_number = get_valid_number_from_range(
            message, from_value=USER_MIN_VALUE, to_value=USER_MAX_VALUE)

        position = make_position(human_number, size=len(board))
        if is_free_position(board, position):
            return position
        print('To jest pole jest już zajęte')

###################################################################################
# LOGIKA GRY

def has_free_field(board):
    for row in board:
        if EMPTY in row:
            return True
    return False

def get_valid_number(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print('podaj jeszcze raz')

def rozpocznij(SIZE):
    result = []
    for _ in range(SIZE):
        row = [EMPTY] * SIZE  # <-- OK
        result.append(row)
    return result

def is_free_position(board, position):
    row, col = position
    return board[row][col] == EMPTY

def has_line(board, symbol):
    def hor(n):
        return all([board[n][it] == symbol for it in range(SIZE)])

    def ver(n):
        return all([board[it][n] == symbol for it in range(SIZE)])

    def cross1():
        return all([board[it][it] == symbol for it in range(SIZE)])

    def cross2():
        return all([board[it][SIZE-1-it] == symbol for it in range(SIZE)])

    horizontals = any([hor(it) for it in range(SIZE)])
    verticals = any([ver(it) for it in range(SIZE)])
    return any([horizontals, verticals, cross1(), cross2()])


def is_end(game):
    return (
            not has_free_field(game['board']) or
            has_line(game['board'], get_player(game))
    )

class BaseUser(abc.ABC):

    @abc.abstractmethod
    def get_position(self, message, board):
        pass

    def make_game(self, user):
        return make_game(user)


class RealUser(BaseUser):

    def get_position(self, message, board):
        return get_position(message, board)

    def make_game(self, user):
        return make_game(user)


class DevUser(BaseUser):

    def __init__(self, seq):
        self.seq = seq
        self.index = 0 if seq else -1

    def get_position(self, message, board):
        if self.index < len(self.seq):
            value = self.seq[self.index]
            self.index += 1
            return make_position(int(value), size=len(board))
        raise Exception('Illegal state')

    def make_game(self, user):
        return make_game(user)

class HistUser(BaseUser):

    def __init__(self, seq):
        self.seq = seq
        self.index = 0 if seq else -1

    def get_position(self, message, board):
        if self.index < len(self.seq):
            value = self.seq[self.index]
            self.index += 1
            while True:
                if input()==' ':
                    print("Pole {} zostalo zajete".format(int(value)))
                    return make_position(int(value), size=len(board))
        raise Exception('Illegal state')

    def make_game(self, user):
        return {
            'board': rozpocznij(SIZE),
            'queue': make_queue(),
            'running': True,
            'user': user,
            'history': self.seq
        }

###################################################################################
# INTERAKCJA Z UŻYTKOWNIKIEM

ANSWER_YES = "y"
ANSWER_NO = "n"

def is_answer(s):
    return s in [ANSWER_YES, ANSWER_NO]

def ask_for_history():
    while True:
        print("czy chcesz odtworzyć grę ?? [y/n]")
        line = input()  #
        answer = line.lower().strip()
        if is_answer(answer):
            return answer == ANSWER_YES

def get_valid_number_from_range(message, from_value, to_value):
    while True:
        number = get_valid_number(message)
        if from_value <= number <= to_value:
            return number
        else:
            print('Wymagana liczba od {} do {}'.format(from_value, to_value))


def make_position(human_number, size):
    index = human_number - 1
    return [index // size, index % size]

def make_human_position(position, size):
    row, col = position
    return row*size + col + 1

def set_board_value(plansza, położenie, player):
    x = położenie[0]
    y = położenie[1]
    plansza[x][y] = player


def make_queue():
    return [PLAYER1, PLAYER2]


def update_queue(queue):
    first, second = queue
    queue[0] = second
    queue[1] = first


def make_game(user):
    return {
        'board': rozpocznij(SIZE),
        'queue': make_queue(),
        'running': True,
        'user': user,
        'history': []
    }


def get_player(game):
    return game['queue'][0]


def update_game(game):
    wyswietl(game['board'])

    print('Ruch wykonuje', get_player(game))  # <---
    position = game['user'].get_position('Podaj pozycję ', game['board'])
    set_board_value(game['board'], position, get_player(game))

    # update_history(game['history'], position)
    game['history'].append(make_human_position(position, SIZE))

    game['running'] = not is_end(game)

    if not game['running']:
        wyswietl(game['board'])
        print("KONIEC GRY!! Wygrał gracz ", get_player(game))

    update_queue(game['queue'])


def run_game(game):
    while game['running']:
        update_game(game)

def main():
    user = DevUser(['2', '6', '3', '7', '4', '9', '1'])
    #user = RealUser()
    game = make_game(user)
    run_game(game)

    display_hist(game)  # Pokazywanie na potrzeby developerskie
    answer = ask_for_history()

    if answer:
        hist_user = HistUser(game['history'])  # <-- BRAWO!
        hist_game = hist_user.make_game(hist_user)
        run_game(hist_game)

    # for _ in range(5):
    # print(user.get_position())




# tests.py
import unittest
class HumanPositionTests(unittest.TestCase):

    def test_when_size_equals_1(self):
        self._run_mini_tests(size=1)

    def test_when_size_equals_2(self):
        self._run_mini_tests(size=2)

    def test_when_size_equals_3(self):
        self._run_mini_tests(size=3)

    def _run_mini_tests(self, size):
        last_number = size * size
        for number in range(1, last_number + 1):
            pos = make_position(number, size)
            human_pos = make_human_position(pos, size)
            self.assertEquals(number, human_pos, 'when size={}'.format(size))


#unittest.main()
main()

# Bibliotka: requests
# requests.get('')


# KOD, KTÓRY URUCHAMIA GRĘ

# pycharm - skroty
# Ctrl+Shift+MINUS
# Ctrl+Shift+PLUS

# TODO:
# dopisz klasę użytkownika pod historię (żeby obsługiwał kliknięcie)

# TODO:
# napisz testy do najważniejszych fragmentów kodu


