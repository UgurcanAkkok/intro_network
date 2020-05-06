import os
import json
import socket

MAX_BYTES = 1024
port = 5001


def log(text):
    with open("download_log.txt", "a") as f:
        f.writelines(text)
    return


def download(chunk, ip):
    successful = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        print("Connected to ", ip)
        filename = {"filename": chunk}
        file_msg = json.dumps(filename)
        sock.sendall(bytes(file_msg, "utf-8"))
        file = os.path.join("file", chunk)
        with open(file, "wb") as f:
            buffer = sock.recv(MAX_BYTES)
            while buffer > 0:
                f.write(buffer)
                buffer = sock.recv(MAX_BYTES)
    except Exception as e:
        print(e)
        successful = False
    return successful


def main():
    while True:
        filename = input("Which file do you want to download? ")
        chunks = [filename + "_" + str(i) for i in range(1,6)]
        content = 0
        with open("content.json", "r") as f:
            content = json.load(f)
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
                print("CHUNK", chunk,
                      "CAN NOT BE DOWNLOADED FROM ONLINE PEERS")


        file_data, addr = sock.recvfrom(MAX_BYTES)
        file = open(file_data, 'wb')
        file.write(file_data)
        file.close()
        print("File has been received successfully.")
    #  except Exception as e:
    #      print(str(e))
    #      pass


if __name__ == "__main__":
    main()
