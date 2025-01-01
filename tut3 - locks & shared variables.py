
# you can ignore logging mechanisms in this file
#  here importing Lock, Value, Process is the most important
from multiprocessing import Process, Lock, Value, get_logger, log_to_stderr
import time
import logging


# this functions adds 500 to the "total" variable
def add_500_lock(total, lock):
    for i in range(100):
        time.sleep(0.01)
        # this lock acquire prevents the other process from using the shared variable "total"
        lock.acquire()
        total.value += 5
        # here releasing the lock means other processes are free to use the "total" variable
        lock.release()


# this functions substracts 500 from the "total" variable
def sub_500_lock(total, lock):
    for i in range(100):
        time.sleep(0.01)
        # same here it prevents other processes from using this "total" variable
        lock.acquire()
        total.value -= 5
        # lock is released so other processes are free to use the "total" variable
        lock.release()


if __name__ == '__main__':
    # ////// ignore this
    #  this just prints info the terminal
    log_to_stderr()
    logger = get_logger()
    logger.setLevel(logging.INFO)
    # ////// ignore this

    # creating the "total" variable which is a shared variable [a common resource]
    total = Value('i', 500)
    # creating a lock
    lock = Lock()

    # creating Processes and remember to send the lock in the arguments (args)
    add_process = Process(target=add_500_lock, args=(total, lock))
    sub_process = Process(target=sub_500_lock, args=(total, lock))

    # basic start and join
    add_process.start()
    sub_process.start()
    add_process.join()
    sub_process.join()
    # after all processes finish the "total" variable's value is printed to the terminal
    print(total.value)
