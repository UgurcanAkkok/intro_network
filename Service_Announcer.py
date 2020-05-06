import glob
import json
import socket
import threading
import time
from datetime import timedelta


MAX_BYTES = 65535

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

def send_msg(MESSAGE, RECEIVER):
    RECEIVER.send(bytes(f"{MESSAGE}", "utf-8"))

def recv_msg(SERVICE):
    MESSAGE, ADDR = SERVICE.recvfrom(MAX_BYTES)
    # STR_MESSAGE = MESSAGE.decode("utf-8")
    print(ADDR, f": {MESSAGE}")
    return MESSAGE, ADDR

def send_bc_msg(FILE_LIST, HOSTED_FILES_LIST, RECEIVER):
    # print(LOCAL_DICT)
    # print("Current files: ", FILE_LIST)
    HOSTED_FILES_LIST = json.dumps(HOSTED_FILES_LIST) # convert JSON array
    # SERVICE_LISTENER.send(bytes(LOCAL_DICT, "utf-8"))
    send_msg(FILE_LIST, RECEIVER)
    send_msg(HOSTED_FILES_LIST, RECEIVER)
    print("Last sent was at ",
          time.ctime())
    print(HOSTED_FILES_LIST)

def register_host(HOST, HOST_ADDR):
    send_msg("Enter username: ", HOST)
    user_name = recv_msg(HOST)
    return user_name

def read_files():
    filenames = glob.glob("files\\*")  # read all files in the directory
    filenames_json = json.dumps(filenames)  # convert JSON array.
    return filenames_json

def main():
    # get files
    file_list = read_files()
    print(file_list)

    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # define UDP server
    # host = socket.gethostname()  # host address
    # port = 2000  # port number

    # defining p2p_server
    SERVICE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # define UDP server
    host = socket.gethostname()  # host address
    port = 8080  # port number
    SERVICE.connect((host, port))  # connect
    print("Connected to "), print(host)
    user_name = register_host(SERVICE, host)
    hosted_msg_dict = {"user_name": [f"{user_name}"],
                       "files": []}
    print(hosted_msg_dict)
    # local_dict = []

    # defining service_listener
    SERVICE_LISTENER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # define UDP server
    host = socket.gethostname()
    port = 5000
    SERVICE_LISTENER.connect((host, port))
    print("Connected to "), print(host)

    # defining thread
    WAIT_TIME_SECONDS = 10
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=send_bc_msg, FILE_LIST=file_list,
              HOSTED_FILES_LIST=hosted_msg_dict, RECEIVER=SERVICE_LISTENER)
    job.start()

    # main loop
    process = True
    while process:
        try:
            file_list = read_files()
            # alert = recv_msg(SERVICE, host)
            # if alert == "0000":
            file_name, addr = recv_msg(SERVICE)
            hosted_msg_dict.get("files").append(str(file_name))
        except Exception as e:
            print(str(e))
            pass


if __name__ == "__main__":
    main()

#     str_client_name = client_name.decode("utf-8")
#     client_time = time.asctime()
#     client_file = s.recv(1024)
#   def register_user(s, local_dict, message_dict):
#     client_info = s.recv(1024)
#     str_client_info = client_info.decode("utf-8")
#     s.send(bytes("Enter username! ", "utf-8"))
#     client_name = s.recv(1024)
#     str_client_name = client_name.decode("utf-8")
#     client_time = time.asctime()
#     client_file = s.recv(1024)
#     if not (str_client_name in message_dict.get("username")):
#         message_dict.get("username").append(str_client_name)
#     str_client_file = client_file.decode("utf-8")
#     local_dict.append((str_client_info, str_client_name, client_time, client_file))
#     message_dict.get("files").append(str_client_file)
#     print("Current users: ", local_dict)
#     print("Hosted files: ", message_dict)
