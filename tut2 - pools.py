# Pools are the same as just creating Process manually but this does it automatically
from multiprocessing import Pool
import time


# sums the squared numbers in sequential manner
def sum_square(number):
    s = 0
    for i in range(number):
        s += i*i
    return s


# sums the squared numbers in Parallel manner
def square_with_MP(numbers):
    start_time = time.time()
    # create a pool variable [class]
    # the Pool("empty") lETS THE POOL DECIDE WHAT NUMBER OF PROCESSES TO CREATE DEPENDING ON YOUR PC
    # we can add a number if we want p = Pool(4)
    p = Pool()

    # creating a result variable that stores the result of the processes
    # as you can see the pool vatiable "p" maps through the numbers array(list)
    # and gives the number to the function
    #  is is the same as process.start()
    result = p.map(sum_square, numbers)
    # // print(result)

    # you must close the pool
    p.close()

    # you can also join the pool to stop anything underneath it from running until it finishes
    p.join()

    #  this is just for time comparison reasons
    end_time = time.time()-start_time
    print(f"MP processing {len(numbers)} takes : {end_time} ")


#  this functions uses sum_square function in a sequential manner
def no_MP(numbers):
    start_time = time.time()
    result = []
    for i in numbers:
        result.append(sum_square(i))
    end_time = time.time()-start_time
    print(f"serial processing {len(numbers)} takes : {end_time} ")


if __name__ == '__main__':
    numbers = range(10000)
    square_with_MP(numbers)
    no_MP(numbers)
