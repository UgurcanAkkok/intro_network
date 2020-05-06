import socket
import threading
import time
from datetime import timedelta

host = socket.gethostname()  # get this pc's host name
port = 8080
MAX_BYTES = 65535

class Job(threading.Thread):  # provides parallel functioning method
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)


def send_msg(MESSAGE, s, ADDRESS):
    s.sendto(bytes(f"{MESSAGE}", "utf-8"), ADDRESS)


def recv_udp_msg(sock):
    MESSAGE, SENDER_HOST = sock.recvfrom(MAX_BYTES)
    STR_MESSAGE = MESSAGE.decode("utf-8")
    print(SENDER_HOST, f": {STR_MESSAGE}")
    return STR_MESSAGE, SENDER_HOST


def send_bc_msg(FILE_LIST, HOSTED_FILES_LIST, RECEIVER):
    print("Connected to "), print(host)
    print("Last sent was at ",
          time.ctime())
    # print(LOCAL_DICT)
    # print("Current files: ", FILE_LIST)
    HOSTED_FILES_LIST = json.dumps(HOSTED_FILES_LIST)  # convert JSON array
    # SERVICE_LISTENER.send(bytes(LOCAL_DICT, "utf-8"))
    send_msg(FILE_LIST, RECEIVER)
    send_msg(HOSTED_FILES_LIST, RECEIVER)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # defining socket object
    s.bind((host, port))
    print(host)
    print("Waiting for any incoming connections ... ")
    msg, addr = recv_udp_msg(s)
    send_msg(input(str(" ")), s, addr)

    ready = True
    # main loop
    while ready:
        try:
            print("Waiting for any incoming connections ... ")
            file_data, downl_addr = recv_udp_msg(s)
            # filename = input(str("Enter the file's name you want to send: "))
            file = open(file_data, 'rb')
            file_data = file.read(1024)
            send_msg(file_data, s, downl_addr)
            print(f"File {file_data} is sent to user {downl_addr} at {time.asctime()}.")
            send_msg(f"{file_data}", s, addr)
        except Exception as e:
            print(str(e))
            pass


if __name__ == "__main__":
    main()
