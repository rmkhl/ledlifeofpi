"""
Show the game of life board on terminal
"""
from . import state
from .config import HEIGHT, WIDTH

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from math import floor


# The "panel" is mounted upside down :)
def _mapping(x, y):
    return (31-x, 31-y)


def run(*, queue, game):
    device = None
    frame = 0
    try:
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, width=HEIGHT, height=WIDTH, block_orientation=90)
        while state.RUNNING:
            board = queue.get()
            # Until there is nothing to show
            if board is None:
                queue.task_done()
                break
            with canvas(device) as draw:
                 for row in range(HEIGHT):
                     for col in range(WIDTH):
                         draw.point(_mapping(col, row), fill="white" if board[col][row] else "black")
            frame += 1
            game(frame)
            queue.task_done()
    finally:
        state.RUNNING = False
        game(None)
