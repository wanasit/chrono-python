#!/usr/bin/python
import os
import sys
import time
import unittest
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

current_dir = os.path.dirname(os.path.realpath(__file__))


class SrcFileEventHandler(PatternMatchingEventHandler):

    patterns = ["*.py"]

    def run_test(self):
        print subprocess.check_output(["python", current_dir + "/test.py"] +
                                      sys.argv[1:])

    def on_modified(self, event):
        self.run_test()

    def on_created(self, event):
        self.run_test()


if __name__ == '__main__':

    handler = SrcFileEventHandler()

    observer = Observer()
    observer.schedule(handler, current_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
