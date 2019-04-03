from . import engine
from . import terminal
import queue
import threading
from functools import partial
from time import sleep

print("Hello world")
sleep(1)

dsp_queue = queue.Queue()
frame_queue = queue.Queue()

threads = []

for t in [
        threading.Thread(
            target=partial(terminal.run, queue=dsp_queue, game=frame_queue.put)),
        threading.Thread(
            target=partial(engine.run, display=dsp_queue.put, sync_queue=frame_queue))
]:
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()

print("That is all folks")
