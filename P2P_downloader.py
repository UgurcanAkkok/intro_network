import socket

MAX_BYTES = 65535
port = 8080


def main():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            host = input(str("Enter host name, please: "))
            sock.connect((host, port))  # connect
            print("Connected to "), print(host)
            sock.send(bytes("files\\transferFile.txt", "utf-8"))

            file_data, addr = sock.recvfrom(MAX_BYTES)
            file = open(file_data, 'wb')
            file.write(file_data)
            file.close()
            print("File has been received successfully.")
        except Exception as e:
            print(str(e))
            pass


if __name__ == "__main__":
    main()
