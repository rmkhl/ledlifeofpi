"""
Game of life main

Start the _THREADS that handle the noise, display and running the game
"""
import queue
import threading
from functools import partial
from time import sleep

from . import engine, noise, state, terminal

print("Hello world")
sleep(1)

_DSP_QUEUE = queue.Queue()
_FRAME_QUEUE = queue.Queue()

_THREADS = []

state.RUNNING = True

for t in [
        threading.Thread(target=noise.run), threading.Thread(target=partial(
            terminal.run, queue=_DSP_QUEUE, game=_FRAME_QUEUE.put)),
        threading.Thread(target=partial(
            engine.run, display=_DSP_QUEUE.put, sync_queue=_FRAME_QUEUE))
]:
    _THREADS.append(t)
    t.start()

# Collect the _THREADS and quit
for thread in _THREADS:
    thread.join()

print("That is all folks")
