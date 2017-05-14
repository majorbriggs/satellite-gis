import time

class Timer:

    def __init__(self, name=''):
        self.name = name

    def __enter__(self):
        print("Started "+self.name)
        self.t0 = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        t = time.time() - self.t0
        print("Execution time of {}: {}".format(self.name, t))