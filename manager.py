from threading import Thread
from time import sleep
import sys

class AcquireManager:
    def __init__(self):
        self.user_using = ''

    def set_user_list(self, user_list):
        self.user_list = user_list

    def acquire(self, ip):
        if   self.user_using != '':
            return False
        elif ip in self.user_list:
            self.user_using = self.user_list[ip]
            return True
        else:
            return False

    def free(self):
        if self.user_using != '':
            self.user_using = ''
            return True
        else:
            return False

class HeartBeatManager():
    def __init__(self):
        self.time_to_live = 0
        self.elapsed = 0
        self.thread = None

    def set_ttl(self, t):
        """How long will you live?"""
        self.time_to_live = t

    def _run(self, callback):
        """Live longer!"""
        self.live()
        while self.elapsed < self.time_to_live:
            sleep(1)
            self.elapsed += 1

        if self.elapsed >= sys.maxsize:
            #Forcedly killed
            return
        else:
            #End of life
            callback()

    def born(self, callback=(lambda: None)):
        """A thread was born in the USA."""
        self.thread = Thread(target=self._run, args=(callback,))
        self.thread.daemon = True
        self.thread.start()

    def live(self):
        """Let the thread come back to life."""
        self.elapsed = 0

    def kill(self):
        """I am the god of hellfire, and I bring you..."""
        self.elapsed = sys.maxsize
