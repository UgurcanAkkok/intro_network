# Copyright (c) 2020
# Yusuf Baran Tanrıverdi, Uğurcan Akkök
# Bahcesehir University.
#
# All rights reserved.


import time
import os
from os import path
import json
import socket
from tqdm import tqdm

MAX_BYTES = 65535
port = 5001


def log(text):
    with open("download_log.txt", "a") as f:
        f.writelines(text)
    return


def combine_chunks(inp, sourcedir, outputdir):
    tqdm.write("Assemblying the chunks ...")
    if not path.exists(outputdir):
        os.makedirs(outputdir)

    with open(path.join(outputdir, inp), 'wb') as outfile:
        t = tqdm(total=5)
        for i in range(1, 6):
            t.set_description("Preparing (file %s)" % inp)
            with open(path.join(sourcedir, inp + "_" + str(i)), "rb") as infile:
                outfile.write(infile.read())
                t.update(1)
        t.close()
    for i in range(1, 6):
        if path.exists(inp + "_" + str(i)):
            os.remove(inp + "_" + str(i))
    tqdm.write("\nFile is ready!")


def download(chunk, ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        # print("Connected to ", ip)
        filename = {"filename": chunk}
        file_msg = json.dumps(filename)
        sock.sendall(bytes(file_msg, "utf-8"))
        file = os.path.join("temp", chunk)
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
        try:
            filename = input("\nWhich file do you want to download? ")
            chunks = [filename + "_" + str(i) for i in range(1, 6)]
            with open("content.json", "r") as f:
                content = json.load(f)
            print(content)
            all_downloaded = True
            t = tqdm(total=5)
            t.set_description("Downloading (file %s)" % filename)
            for chunk in chunks:
                if chunk in content:
                    users = content[chunk]
                    downloaded = False
                    for user in users:
                        if download(chunk, user) is True:
                            downloaded = True
                            t.update(1)
                            break
                        else:
                            downloaded = False
                    if downloaded is False:
                        t.close()
                        all_downloaded = False
                        t.write("\n CHUNK %s CAN NOT BE DOWNLOADED FROM ONLINE PEERS (err1002)" % chunk)
                else:
                    t.close()
                    t.write("\n CHUNK %s CAN NOT BE DOWNLOADED FROM ONLINE PEERS" % chunk)
                    all_downloaded = False
                    break
            if all_downloaded:
                t.close()
                # tqdm.write("\nAll chunks are successfully downloaded.")
                combine_chunks(filename, "files", "files")
        except Exception as e:
            print("\n", e)
            pass


if __name__ == "__main__":
    main()
