import time
import os
from os import path
import json
import socket

MAX_BYTES = 1024
port = 5001


def log(text):
    with open("download_log.txt", "a") as f:
        f.writelines(text)
    return


def combine_chunks(inp, sourcedir, outputdir):
    if not path.exists(outputdir):
        os.makedirs(outputdir)
    with open(path.join(outputdir, inp), 'wb') as outfile:
        for i in range(1, 6):
            with open(path.join(sourcedir, inp + "_" + str(i)), "rb") as infile:
                outfile.write(infile.read())
    for i in range(1, 6):
        if path.exists(inp + "_" + str(i)):
            os.remove(inp + "_" + str(i))


def download(chunk, ip):
    successful = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        print("Connected to ", ip)
        filename = {"filename": chunk}
        file_msg = json.dumps(filename)
        sock.sendall(bytes(file_msg, "utf-8"))
        file = os.path.join("files", chunk)
        with open(file, "wb") as f:
            buffer = sock.recv(MAX_BYTES)
            while len(buffer) > 0:
                f.write(buffer)
                buffer = sock.recv(MAX_BYTES)
    except Exception as e:
        print(e)
        successful = False
    else:
        successful = True
    if successful:
        log(f"File {chunk} is downloaded from the user \
                {ip} at {time.ctime()}.")
    sock.close()
    return successful


def main():
    while True:
        filename = input("Which file do you want to download? ")
        chunks = [filename + "_" + str(i) for i in range(1, 6)]
        content = 0
        with open("content.json", "r") as f:
            content = json.load(f)
        all_downloaded = True
        for chunk in chunks:
            users = content[chunk]
            downloaded = False
            for user in users:
                if download(chunk, user) is True:
                    downloaded = True
                    break
                else:
                    downloaded = False
                    continue
            if downloaded is False:
                all_downloaded = False
                print("CHUNK", chunk,
                      "CAN NOT BE DOWNLOADED FROM ONLINE PEERS")
        if all_downloaded:
            print("All chunks are successfully downloaded.")
            print("Assemblying the chunks")
            combine_chunks(filename, "files", "files")


if __name__ == "__main__":
    main()
