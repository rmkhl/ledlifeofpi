from curses import wrapper, ERR
from functools import partial

from .engine import width, height

emit = None


def worker(screen, *, queue, game):
    frame = 0
    # Show the board and send back info on what frame we did
    screen.nodelay(True)
    while screen.getch() == ERR:
        board = queue.get()
        # Until there is nothing to show
        if board is None:
            game(None)
            queue.task_done()
            break
        screen.clear()
        for row in range(height):
            for col in range(width):
                screen.addch(row, 2 * col, "O" if board[row][col] else " ")
        frame += 1
        screen.addstr(height, 0, 'frame: {frame}'.format(frame=frame))
        screen.refresh()
        game(frame)
        queue.task_done()

    game(None)


def run(queue, game):
    global emit

    fn = partial(worker, queue=queue, game=game)
    wrapper(fn)
