# Copyright (c) 2020
# Yusuf Baran Tanrıverdi, Uğurcan Akkök
# Bahcesehir University.
#
# All rights reserved.


import socket
import logging as log
import json

localhost = ""
port = 5000
MAX_BYTES = 65535
# content = {}



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
    print(f"user:{data['username']}\nfiles: {data['files']}")
    return


def add_content(data, ip, content):

    print("0) content here: ", content)
    files = data["files"]
    for file in files:
        if content.get(file, None) is None:
            content[file] = [ip]
        else:
            if ip not in content[file]:
                content[file] += [ip]
    dump_content(content)
    return


def dump_content(content):
    print("1) content here: ", content)
    with open("content.json", "w") as f:
        json.dump(content, f)
    return


def main():

    log.basicConfig(level=log.ERROR)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((localhost, port))
    log.info(f"Listening at {sock.getsockname()}.")
    print(f"Listening at {sock.getsockname()}.")

    while True:
        content = {}
        data, addr = sock.recvfrom(MAX_BYTES)
        log.info(f"Recieved data is {data}\nAddress is {addr}")
        print(f"Recieved data is {data}\nAddress is {addr}")
        try:
            data = json.loads(data)
            check_data_json(data)
            print_service(data)
            add_content(data, addr[0], content)
        except json.JSONDecodeError as e:
            log.warning("Can not read the received data as json")
            log.warning("Received message is:")
            log.warning(e.doc)


if __name__ == "__main__":
    main()
