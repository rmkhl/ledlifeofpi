"""
Game of Life engine with a noisy twist
"""
from collections import deque
from functools import reduce
from time import sleep

from . import noise, state
from .config import FRAME_DELAY, HEIGHT, WIDTH


def _empty_board():
    """Create an empty board (two dimensional "array" of HEIGHTxWIDTH)"""
    return [
        row for row in [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
    ]


def _cell(y_off, x_off, y, x):  # pylint: disable=invalid-name
    """return cell relative to y, x (board wraps around both in y and x directions)"""
    return (y + HEIGHT + y_off) % HEIGHT, (x + WIDTH + x_off) % WIDTH


def _next_state(board):
    """calculate the next state of the board according to the rules"""
    new_board = _empty_board()

    # pylint: disable=invalid-name
    for yy in range(HEIGHT):
        for xx in range(WIDTH):
            # abusing the fact that True == 1 and False == 0
            p = reduce(lambda a, b: a + b, [
                board[y][x]
                for y, x in [
                    _cell(y_off, x_off, yy, xx)
                    for y_off, x_off in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (
                        0, 1), (1, -1), (1, 0), (1, 1)]
                ]
            ])
            if board[yy][xx]:
                new_board[yy][xx] = p in [2, 3]
            else:
                new_board[yy][xx] = p == 3
    return new_board


def _stalled(boards):
    """Check if the game has stalled (static or alternating between two states)"""
    return (boards[0] == boards[2]) or (boards[1] == boards[2])


def run(display, sync_queue):
    """Run the game of life"""
    while not noise.available():
        sleep(0.2)

    # simplify the logic by assuming we have already run two steps
    # then add the starting board of pure noise as the next one
    # to be displayed
    boards = deque([[], []])
    board = _empty_board()
    noise.add(board)
    boards.append(board)

    # now we can run the game without too much trouble
    try:
        while state.RUNNING:
            # Show current state of the game
            display(board)
            frame = sync_queue.get()
            if frame is None:  # if there was a display issue, quit
                break
            sleep(FRAME_DELAY)

            # calculate next state and add noise if the game has stalled
            board = _next_state(board)
            boards.popleft()
            boards.append(board)
            if _stalled(boards):
                noise.add(board)
    finally:
        state.RUNNING = False
        display(None)  # tell the display we are quitting
