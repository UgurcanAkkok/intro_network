import os
from os import path
import math
import socket
#  import threading
import time
import json
import re
#  from datetime import timedelta

host = ""
port = 5001
MAX_BYTES = 65535


def divide_into_chunks(file, fileName, directory):
    if not path.exists(directory):
        os.makedirs(directory)
    c = path.getsize(file)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)
    cnt = 1
    with open(file, 'rb') as infile:
        divided_file = infile.read(int(CHUNK_SIZE))
        while divided_file:
            name = path.join(directory, fileName.split('.')[0] + "_" + str(cnt))
            with open(name, 'wb+') as div:
                div.write(divided_file)
            cnt += 1
            divided_file = infile.read(int(CHUNK_SIZE))


def combine_chunks(inp,sourcedir,outputdir):
    if not path.exists(outputdir):
        os.makedirs(outputdir)
    with open(path.join(outputdir, inp), 'wb') as outfile:
        for i in range(1, 6):
            with open(path.join(sourcedir, inp + "_" + str(i)), "rb") as infile:
                outfile.write(infile.read())
    for i in range(1, 6):
        if path.exists(inp + "_" + str(i)):
            os.remove(inp + "_" + str(i))


def send_msg(MESSAGE, s, ADDRESS):
    s.sendto(bytes(f"{MESSAGE}", "utf-8"), ADDRESS)


#  def recv_udp_msg(sock):
#      MESSAGE, SENDER_HOST = sock.recvfrom(MAX_BYTES)
#      STR_MESSAGE = MESSAGE.decode("utf-8")
#      print(SENDER_HOST, f": {STR_MESSAGE}")
#      return STR_MESSAGE, SENDER_HOST


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


def ls():
    r = re.compile(r"(.*)_\d+$")
    all_files = os.listdir("files")
    print(all_files)
    files = set()
    for f in all_files:
        match = r.match(f)
        if match is not None:
            files.add(match.groups()[0])
        else:
            files.add(f)

    return files


def main():

    print(ls())
    while True:
        initial_file = input("Which file to host initially?")
        initial_file_path = path.join("files",initial_file)
        if path.isfile(initial_file_path):
            divide_into_chunks(initial_file_path, initial_file, "files")
            print("Ready to host",initial_file,".")
            break
        else:
            print("Check the file name")
            continue

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defining socket object
    s.bind((host, port))
    s.listen()
    #  msg, addr = recv_udp_msg(s)
    #  send_msg(input(str(" ")), s, addr)

    # main loop
    while True:
        try:
            print("Waiting for any incoming connections at",s.getsockname(),"...")
            #  file_data, downl_addr = recv_udp_msg(s)
            #  filename = input(str("Enter the file's name you want to send: "))
            sc, addrinfo = s.accept()
            print("We have incoming message from", addrinfo)
            msg = sc.recv(1024)
            msg = json.loads(msg)
            filename = msg["filename"]
            with open(filename, 'rb') as file:
                sc.sendfile(file)
            print(f"File {filename} is sent to user {addrinfo} at {time.ctime()}.")
            sc.close()
        except Exception as e:
            print(str(e))
            pass


if __name__ == "__main__":
    main()
