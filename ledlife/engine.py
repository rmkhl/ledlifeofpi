# Simple implementation of conveys game of life
from random import randint
from time import sleep
from . import noise
from functools import reduce

width = 32
height = 32

frames_per_second = 1


def _empty_board():
    return [
        row for row in [[False for _ in range(width)] for _ in range(height)]
    ]


def _cell(y_off, x_off, y, x):
    return (y + height + y_off) % height, (x + width + x_off) % width


def _next_state(board):
    new_board = _empty_board()

    for yy in range(height):
        for xx in range(width):
            # abusing the fact that True == 1 and False == 0
            p = reduce(lambda a, b: a + b, [
                board[y][x] for y, x in [_cell(y_off, x_off, yy, xx) for y_off, x_off in [
                    (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]]])
            if board[yy][xx]:
                new_board[yy][xx] = p in [2, 3]
            else:
                new_board[yy][xx] = p == 3
    return new_board


class FrameError(Exception):
    pass


def run(display, sync_queue):
    board = _empty_board()
    # Start with a random board
    try:
        noise.add(board=board, height=height, width=width)
        while True:
            display(board)
            frame = sync_queue.get()
            if frame is None:
                sync_queue.task_done()
                raise FrameError()
            board = _next_state(board)
            sync_queue.task_done()
            sleep(0.2)
        display(None)
    except FrameError:
        pass
    except:
        display(None)
        raise
