import os
from os import path
import math
import socket
import time
import json
import re
from tqdm import tqdm

host = ""
port = 5001
MAX_BYTES = 1024


def log(text):
    with open("server_log.txt", "a") as f:
        f.writelines(text)
    return


def divide_into_chunks(file, fileName, directory):
    if not path.exists(directory):
        os.makedirs(directory)
    c = path.getsize(file)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)
    cnt = 1
    # fileName, ext = path.splitext(fileName) # if ext to be seperated.
    with open(file, 'rb') as infile:
        divided_file = infile.read(int(CHUNK_SIZE))
        while divided_file:
            for i in tqdm(range(5)):
                name = path.join(directory, fileName + "_" + str(cnt))
                with open(name, 'wb+') as div:
                    div.write(divided_file)
                cnt += 1
                divided_file = infile.read(int(CHUNK_SIZE))



def ls():
    r = re.compile(r"(.*)_\d+$")
    all_files = os.listdir("files")
    files = set()
    for f in all_files:
        match = r.match(f)
        if match is not None:
            files.add(match.groups()[0])
        else:
            files.add(f)

    return files


def update_chunks(files: set):
    new_files = ls()
    if files != new_files:
        #Ask to update the chunks
        ask_for_file(new_files)
    return new_files

def ask_for_file(file_list):
    print(file_list)
    while True:
        file = input("Which file to ready for hosting? ")
        file_path = path.join("files", file)
        if path.isfile(file_path):
            divide_into_chunks(file_path, file, "files")
            print("Ready to host", file, ".")
            break
        else:
            ans = input("Cancelling file preparation ok?(yes/no)")
            if ans == "yes":
                break
            else:
                print("Check the filename..")
                continue
    return


def main():
    file_list = ls()
    ask_for_file(file_list)
    # defining socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    sc = 0
    # main loop
    while True:
        try:
            file_list = update_chunks(file_list)
            print("Waiting for any incoming connections at",
                  s.getsockname(), "...")
            sc, addrinfo = s.accept()
            # for i in tqdm(range(5)):
            print("We have incoming message from", addrinfo)
            msg = sc.recv(MAX_BYTES)
            msg = json.loads(msg)
            filename = path.join("files", msg["filename"])
            with open(filename, 'rb') as file:
                sc.sendfile(file)
                log_text = "File {} is sent to user {} at {}." \
                    .format(msg["filename"], addrinfo, time.ctime())
                str.format
                log(log_text)
        except Exception as e:
            print(str(e))
            pass
    sc.close()


if __name__ == "__main__":
    main()
