from itertools import accumulate
import numpy as np
import time
from bdb import Bdb
import sys
def fast_sorted_arr(size):
    return [int(4*a) - size for a in accumulate(np.random.rand(1,size)[0])]

def test_speed(func):
    n = 10
    bin_search_time = 0
    index_time = 0
    size = 100000
    for i in range(n):
        arr = fast_sorted_arr(size)
        key = arr[np.random.randint(0,size)]

        start = time.time()
        arr.index(key)
        end = time.time()
        index_time += end - start

        start = time.time()
        func(arr, key)
        end = time.time()
        bin_search_time += end - start
    return 2*bin_search_time < index_time


# adapted from https://stackoverflow.com/questions/36662181/is-there-a-way-to-check-if-function-is-recursive-in-python
class RecursionDetected(Exception):
    pass

class RecursionDetector(Bdb):
    def do_clear(self, arg):
        pass

    def __init__(self, *args):
        Bdb.__init__(self, *args)
        self.stack = set()

    def user_call(self, frame, argument_list):
        code = frame.f_code
        if code in self.stack:
            raise RecursionDetected
        self.stack.add(code)

    def user_return(self, frame, return_value):
        self.stack.remove(frame.f_code)

def test_recursion(func, *args):
    detector = RecursionDetector()
    detector.set_trace()
    try:
        func(*args)
    except RecursionDetected:
        return True
    else:
        return False
    finally:
        sys.settrace(None)
