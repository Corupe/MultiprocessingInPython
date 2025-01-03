import multiprocessing

def worker(shared_list, shared_dict, lock, value):
    """Worker function that modifies shared list and dictionary."""
    with lock:  # Locking ensures safe access to shared data
        shared_list.append(value)
        shared_dict[value] = value ** 2

if __name__ == "__main__":
    # Create a manager to handle shared objects
    with multiprocessing.Manager() as manager:
        # Create shared list and dictionary
        shared_list = manager.list()
        shared_dict = manager.dict()
        
        # Create a Lock to synchronize access
        lock = manager.Lock()
        
        # Create a list of processes
        processes = []
        for i in range(5):
            p = multiprocessing.Process(target=worker, args=(shared_list, shared_dict, lock, i))
            processes.append(p)
            p.start()
        
        # Wait for all processes to finish
        for p in processes:
            p.join()
        
        # Print the shared data
        print("Shared List:", shared_list)
        print("Shared Dictionary:", shared_dict)