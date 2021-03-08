import socket
import queue
import threading
q = queue.Queue()
def scan():
    ip = "127.0.0.1"

    while not q.empty():
        port = q.get()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = client.connect_ex((ip,port))
        if result == 0:
            print(str(port)+'open')
            with open('./portList.txt','a+',encoding='utf8') as file:
                file.write(str(port)+"open\n")
        else:
            print(str(port)+'close')
        client.close()
if __name__ == '__main__':
    for port in range(1, 65536):
        q.put(port)
    for _ in range(20):
        t = threading.Thread(target=scan)
        t.start()