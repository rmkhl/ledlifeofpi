"""
Generate noise for the game of life board
"""
from threading import Lock
from time import sleep

import picamera
import picamera.array

from . import state
from .config import CAPTURE_INTERVAL, HEIGHT, WIDTH

# Image frame (two images) and the lock to guard the access
_IMAGE_LOCK = Lock()
_IMAGES = [[], []]


def _capture(frame):
    """Capture camera image as "noise" and save it to image frame"""
    _IMAGE_LOCK.acquire()
    with picamera.PiCamera() as camera:
        _IMAGES[frame] = []
        with picamera.array.PiRGBArray(camera) as stream:
            camera.resolution = (WIDTH, HEIGHT)
            camera.capture(stream, 'rgb')
            for row in stream.array:
                _IMAGES[frame].append(
                    [int(sum(col) / len(col)) for col in row])
    _IMAGE_LOCK.release()


def run():
    """run the capture constantly (should be started as an independent thread)"""
    try:
        _capture(0)
        img = 1
        while state.RUNNING:
            _capture(img)
            img = 0 if img else 1
            sleep(CAPTURE_INTERVAL)
    finally:
        state.RUNNING = False


def add(board):
    """Interface for the game engine to add noise to given board"""
    _IMAGE_LOCK.acquire()
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if _IMAGES[0][row][col] != _IMAGES[1][row][col]:
                board[row][col] = True
    _IMAGE_LOCK.release()


def available():
    """Check if there are frames that can be used to generate noise"""
    _IMAGE_LOCK.acquire()
    running = (_IMAGES[0] and _IMAGES[1]) and _IMAGES[0] != _IMAGES[1]
    _IMAGE_LOCK.release()
    return running
