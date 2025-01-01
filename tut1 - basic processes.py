# DISCLAIMER AND NOTICES :
#   1: you can remove time.sleep(0.5) from the square_numbers function
#   2: you can lower the amount of processes to a range from 1 to 4
#   3: ask any time to explain any of this


# multiprocessing : a standard library that comes installed with python, it let's us make parallel programs
from multiprocessing import Process, current_process

# time : a standard library that comes installed with python,
# it let's us use time functions like knowing the time now, also it can be used to delay functions.
import time


# square_numbers : a function that receives an array of numbers and prints the squared number
def square_numbers(numbers: []):
    # created this "result" list(array/table) to hold the squared results of each number
    result = []
    # just a loop that goes through each nulber and squeres it then appending it to the result list(array)
    for number in numbers:
        # time.sleep(seconds) : this delays the code by half a second
        # time.sleep(0.5)
        # adding the squared number to the list(array) "result"
        result.append(number*number)
    # printing the final list(array)
    print(result)


# احفظوها ذي
if __name__ == '__main__':
    start = time.time()
    # numbers is a list of 100 numbers(0 included), it looks like this numbers = [0,1,2,3,4,5,6.....,98,99]
    numbers = range(100000)
    # created an empty list for processes [example : p1 = Process(target=function, args=(arguments,))]
    processes = []
    # imagine like this for(int i = 0; i < 50; i++){bla bla bla}
    for i in range(5):
        # here creating a Process that receives square_numbers as a target function and numbers as an argument for square_numbers
        process = Process(target=square_numbers, args=(numbers,))
        #  just adding the processes to an array
        processes.append(process)
        # then starting each Process independently
        process.start()

    # here just looping to stop any work under these Processes from starting until they finish
    for process in processes:

        process.join()
    #  the above loop is stoping this from working until they finish the work
    end = time.time() - start
    print(f"multi processing finished in {end}")
