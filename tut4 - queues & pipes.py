from multiprocessing import Process, Pipe
import time


def producer(conn, queue_range):
    # Using the connection's send end
    for i in range(queue_range):
        print(f"Producing: {i}")
        conn.send(i)
        time.sleep(0.2)
    # Send None to signal the end of the queue
    conn.send(None)
    # Close the connection when done
    conn.close()


def consumer(conn):
    # Using the connection's receive end
    while True:
        item = conn.recv()  # Receive data from the pipe
        if item is None:  # If we receive None, stop consuming
            break
        print(f"Consuming: {item}")
    # Close the connection when done
    conn.close()


if __name__ == "__main__":
    # This returns a tuple of (receive_connection, send_connection)
    # queue = Queue()  # This is a simple queue we can use instead of a pipe
    recv_conn, send_conn = Pipe()
    # Define range of items to produce
    queue_range = 50

    # Create processes with pipe connections
    producer_process = Process(target=producer, args=(send_conn, queue_range))
    consumer_process = Process(target=consumer, args=(recv_conn,))

    # Start both processes
    producer_process.start()
    consumer_process.start()

    # Wait for both processes to complete
    producer_process.join()
    consumer_process.join()
