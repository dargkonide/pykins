import threading
import inspect
import ctypes

def _async_raise(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
 
class Thread(threading.Thread):
    def _get_my_tid(self):
        if not self.is_alive():
            raise threading.ThreadError("the thread is not active")
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid
        raise AssertionError("could not determine the thread's id")
 
    def raise_exc(self, exctype):
        _async_raise(self._get_my_tid(), exctype)
 
    def terminate(self):
        self.raise_exc(SystemExit)

import time

def f():
    try:
        while True:
            time.sleep(10)
    finally:
        print ("outta here")

t = Thread(target = f)
t.start()
print(t.is_alive())
t.terminate()
t.join()
print(t.is_alive())