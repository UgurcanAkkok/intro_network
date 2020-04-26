import socket
import time
from multiprocessing import Process
import glob
import os
import json


def run_in_parallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def register_user(s, local_dict):
    try:
        client_info = s.recv(1024)
        str_client_info = client_info.decode("utf-8")
        s.send(bytes("Enter username! ", "utf-8"))
        client_name = s.recv(1024)
        str_client_name = client_name.decode("utf-8")
        client_time = time.asctime()
        client_file = s.recv(1024)
        str_client_file = client_file.decode("utf-8")
        local_dict.append((str_client_info, str_client_name, client_time, client_file))
        print(local_dict)
    except Exception as e:
        print(str(e))
        pass


def count_time(local_dict, tic_, toc_):
    print(local_dict)

    while True:
        clock = tic_ - toc_
        if int(clock) % 60 == 0:
            print(local_dict)
            print(" last update was at the time: " + time.asctime())


def main():
    # print(glob.glob("*"))
    filenames = glob.glob("*")  # read all files in the directory
    filenames_json = json.dumps(filenames)  # convert JSON array.
    tic = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 8080
    s.connect((host, port))
    print("Connected ... ")

    msg = s.recv(1024)
    print("Host: ", msg.decode("utf-8"))
    s.send(bytes("Hello World, I connected. I am your Announcer.", "utf-8"))
    s.send(bytes("Code0001", "utf-8"))

    ready = False
    alert = s.recv(1024)
    str_alert = alert.decode("utf-8")
    print("Host: ", str_alert)
    code = s.recv(8)
    str_code = code.decode("utf-8")
    print("Host: ", str_code)
    if str_code == "Code0000":
        s.send(bytes(filenames_json, "utf-8"))
        ready = True
    print(ready)
    local_dict = []
    register_user(s, local_dict)
    while True:
        run_in_parallel(register_user(s, local_dict), count_time(local_dict, tic, time.time()))


if __name__ == "__main__":
    main()
