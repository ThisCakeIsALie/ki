import time

class Stopwatch(object):
    def __init__(self):
        self._start_time = None
        self._stop_time = None

    def start(self):
        self._start_time = time.time()
        
    def stop(self):
        self._stop_time = time.time()

    def elapsed(self):
        return self._stop_time - self._start_time
