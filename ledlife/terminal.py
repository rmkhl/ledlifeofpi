"""
Show the game of life board on terminal
"""
import curses

from . import state
from .config import HEIGHT, WIDTH


def worker(screen, *, queue, game):
    """Get board updates and show them on the terminal"""
    frame = 0
    # Show the board and send back info on what frame we did
    try:
        screen.nodelay(True)
        while state.RUNNING and screen.getch() == curses.ERR:
            board = queue.get()
            # Until there is nothing to show
            if board is None:
                queue.task_done()
                break
            screen.clear()
            for row in range(HEIGHT):
                for col in range(WIDTH):
                    screen.addch(row, 2 * col, "O" if board[row][col] else " ")
            frame += 1
            screen.addstr(HEIGHT, 0, 'frame: {frame}'.format(frame=frame))
            screen.refresh()
            game(frame)
            queue.task_done()
    finally:
        state.RUNNING = False
        game(None)


def run(*, queue, game):
    """Initialize curses and start the actual worker"""
    try:
        screen = curses.initscr()
        curses.cbreak()
        worker(screen, queue=queue, game=game)
    finally:
        curses.nocbreak()
        curses.endwin()
