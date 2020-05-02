import glob
import json
import socket
import threading
import time
from datetime import timedelta


def send_broadcast(FILE_LIST, LOCAL_DICT, RECEIVER):
    print("Last check was at ",
          time.ctime())
    print(LOCAL_DICT)
    FILE_LIST = json.dumps(FILE_LIST)  # convert JSON array.
    print("Current files: ", FILE_LIST)
    LOCAL_DICT = json.dumps(LOCAL_DICT)
    RECEIVER.send(bytes(LOCAL_DICT, "utf-8"))
    RECEIVER.send(bytes(FILE_LIST, "utf-8"))


class Job(threading.Thread):
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


def register_user(s, local_dict, message_dict):
    client_info = s.recv(1024)
    str_client_info = client_info.decode("utf-8")
    s.send(bytes("Enter username! ", "utf-8"))
    client_name = s.recv(1024)
    str_client_name = client_name.decode("utf-8")
    client_time = time.asctime()
    client_file = s.recv(1024)
    if not (str_client_name in message_dict.get("username")):
        message_dict.get("username").append(str_client_name)
    str_client_file = client_file.decode("utf-8")
    local_dict.append((str_client_info, str_client_name, client_time, client_file))
    message_dict.get("files").append(str_client_file)
    print("Current users: ", local_dict)
    print("Hosted files: ", message_dict)


def main():
    # print(glob.glob("*"))
    filenames = glob.glob("*")  # read all files in the directory
    filenames_json = json.dumps(filenames)  # convert JSON array.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 8080
    s.connect((host, port))
    print("Connected ... ")
    local_dict = []
    message_dict = {"username": [],
                    "files": []}
    WAIT_TIME_SECONDS = 60
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=send_broadcast, FILE_LIST=filenames,
              LOCAL_DICT=message_dict, RECEIVER=s)
    job.start()

    msg = s.recv(1024)
    print("Host: ", msg.decode("utf-8"))
    s.send(bytes("Hello World, I connected. I am your Announcer.", "utf-8"))
    s.send(bytes("Code0001", "utf-8"))

    ready = False
    code = s.recv(8)
    str_code = code.decode("utf-8")
    print("Host: ", str_code)
    if str_code == "Code0000":
        s.send(bytes(filenames_json, "utf-8"))
        ready = True
    print(ready)
    while ready:
        filenames = glob.glob("*")  # read all files in the directory if anything is added
        register_user(s, local_dict, message_dict)


if __name__ == "__main__":
    main()
