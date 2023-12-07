import threading


class ReadWriteLock:
    def __init__(self):
        self._lock = threading.Lock()
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._read_count = 0

    def acquire_read(self):
        with self._lock:
            self._read_count += 1
            if self._read_count == 1:
                self._write_lock.acquire()
        self._read_lock.acquire()

    def release_read(self):
        self._read_lock.release()
        with self._lock:
            self._read_count -= 1
            if self._read_count == 0:
                self._write_lock.release()

    def acquire_write(self):
        self._write_lock.acquire()

    def release_write(self):
        self._write_lock.release()
