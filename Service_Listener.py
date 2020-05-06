import socket
import logging as log
import json
import time
import threading
from datetime import timedelta

localhost = ""
port = 5000
MAX_BYTES = 1024
content = {}


def recv_msg(SENDER, SENDER_HOST):
    MESSAGE = SENDER.recv(MAX_BYTES)
    STR_MESSAGE = MESSAGE.decode("utf-8")
    print(SENDER_HOST, f": {STR_MESSAGE}")
    return STR_MESSAGE


def receive_bc_msg(SENDER, ADDR):  # receive periodic messages
    FILES_LIST = recv_msg(SENDER, ADDR)
    HOSTED_FILES_LIST = recv_msg(SENDER, ADDR)
    print(f"{ADDR} sent at {time.ctime()}")
    return


def check_data_json(data):
    try:
        data["username"]
        if not type(data["files"]) is list:
            log.error("Incorrect file list type")
    except KeyError as e:
        log.error("Received data has incorrect format")
        log.error(str(e))
    return


def print_service(data):
    print(f"user:{data['username']}\nfiles:")
    print(f"File list (type is {type(data['files'])}: {data['files']}")
    return


def add_content(data, ip):
    files = data["files"]
    for file in files:
        if content.get(file, None) is None:
            content[file] = [ip]
        else:
            if ip not in content[file]:
                content[file] += [ip]
    dump_content()
    return


def dump_content():
    with open("content.json", "w") as f:
        json.dump(content, f)
    return


def main():
    log.basicConfig(level=log.INFO)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((localhost, port))
    log.info(f"Listening at {sock.getsockname()}.")
    print(f"Listening at {sock.getsockname()}.")

    while True:
        data, addr = sock.recvfrom(MAX_BYTES)
        log.info(f"Recieved data is {data}\nAddress is {addr}")
        print(f"Recieved data is {data}\nAddress is {addr}")
        try:
            data = json.loads(data)
            check_data_json(data)
            print_service(data)
            add_content(data, addr[0])
        except json.JSONDecodeError as e:
            log.warning("Can not read the received data as json")
            log.warning("Received message is:")
            log.warning(e.doc)


if __name__ == "__main__":
    main()
