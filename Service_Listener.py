import socket
import logging as log
import json

port = 5000
MAX_BYTES = 65535
content = {}


def check_data_json(data):
    try:
        data["username"]
        data["files"]
    except KeyError as e:
        log.error("Received data has incorrect format")
        log.error(str(e))
    return


def print_service(data):
    print(f"user:{data['username']}\nfiles:")
    print(data["files"])
    return


def add_content(data, ip):
    files = data["files"]
    for file in files:
        if content.get(file, None) is None:
            content[file] = [ip]
        else:
            content[file] += [ip]
    dump_content()
    return


def dump_content():
    with open("content.json") as f:
        json.dump(content, f)
    return


def main():
    log.basicConfig(level=log.INFO)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    localhost = socket.gethostbyname("localhost")
    sock.bind((localhost, port))
    log.info(f"Listening at {sock.getsockname()}")
    while True:
        data, addr = sock.recvfrom(MAX_BYTES)
        log.info(f"Recieved data is {data}\nAddress is {addr}")
        try:
            data = json.loads(data)
            check_data_json(data)
            print_service(data)
            add_content(data, addr[0])
        except json.JSONDecodeError as e:
            log.warning("Can not read the received data as json")
            log.warning("Received message is:")
            log.warning(e.doc)

    return


if __name__ == "__main__":
    main()
