from .config import HEIGHT, WIDTH
from random import randint


def add(board):
    for _ in range(int(HEIGHT * WIDTH / 8)):
        board[randint(0, HEIGHT - 1)][randint(0, WIDTH - 1)] = True
