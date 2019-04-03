from random import randint


def add(*, board, height, width):
    for _ in range(int(height * width / 4)):
        board[randint(0, height - 1)][randint(0, width - 1)] = True
