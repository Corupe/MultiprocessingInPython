from multiprocessing import Process, Event

def wait_for_event(event):
    print("Waiting for event to be set...")
    event.wait()
    print("Event is set!")

if __name__ == "__main__":
    event = Event()
    p = Process(target=wait_for_event, args=(event,))
    p.start()

    print("Setting event...")
    event.set()
    p.join()