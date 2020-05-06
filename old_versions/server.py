import socket
import threading
import time
from datetime import timedelta


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defining socket object
host = socket.gethostname()  # get this pc's host name
port = 8080
s.bind((host, port))
s.listen(2)  # maximum listener number (increase that maybe)
print(host)
print("Waiting for any incoming connections ... ")
ann, addr = '', ''


def receive_broadcast(SENDER):  # receive periodic messages
    MESSAGE = SENDER.recv(2048)
    MESSAGE_toSTR = MESSAGE.decode("utf-8")
    print("Dictionary: ", MESSAGE_toSTR)
    FILES = SENDER.recv(2048)
    FILES_toSTR = FILES.decode("utf-8")
    print("Dictionary: ", FILES_toSTR)


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


launch = False
while not launch:  # firstly connect the announcer
    ann, addr = s.accept()
    print(addr, "Has connected to the server")
    ann.send(bytes("Welcome to the server", "utf-8"))
    ans = ann.recv(1024)
    str_ans = ans.decode("utf-8")
    print(addr, ": ", str_ans)
    code = ann.recv(8)
    str_code = code.decode("utf-8")
    if str_code == "Code0001":
        ann.send(bytes("Code0000", "utf-8"))
        files = ann.recv(1024)
        launch = True
        print(launch)

print(addr, " is Service_Announcer")
ready = True
# print(ready)
WAIT_TIME_SECONDS = 60
job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS),
          execute=receive_broadcast, SENDER=ann)
job.start()

while ready:
    try:
        print("Waiting for any incoming connections ... ")
        client, address = s.accept()
        print(address, "Has connected to the server")
        client.send(bytes("Welcome to the server", "utf-8"))
        ans = client.recv(1024)
        str_ans = ans.decode("utf-8")
        print(address, ": ", str_ans)
        ann.send(bytes(f"{address}", "utf-8"))
        alert = ann.recv(1024)
        str_alert = alert.decode("utf-8")
        print("Announcer: ", str_alert)
        client.send(bytes(f"Announcer: {str_alert}", "utf-8"))
        user_name = client.recv(1024)
        str_user_name = user_name.decode("utf-8")
        print(address, ": My user name is ", str_user_name)
        ann.send(bytes(f"{str_user_name}", "utf-8"))
        ready_toFT = True
        print(ready_toFT)
        if ready_toFT:
            filename = input(str("Enter the file's name you want to send: "))
            file = open(filename, 'rb')
            file_data = file.read(1024)
            client.send(bytes(file_data))
            print(
                f"File {filename} is sent to user {str_user_name} at {time.asctime()}.")
            ann.send(bytes(f"{filename}", "utf-8"))
    except Exception as e:
        print(str(e))
        pass
