import socket
import threading
from queue import Queue

def scan_port(target, port, timeout, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except Exception as e:
        pass

def worker(target, port_queue, timeout, open_ports):
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(target, port, timeout, open_ports)
        port_queue.task_done()

def scan_ports(target, start_port, end_port, num_threads=100, timeout=1):
    open_ports = []
    port_queue = Queue()

    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(target, port_queue, timeout, open_ports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return open_ports
