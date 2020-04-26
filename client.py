
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input(str("Please enter the host address of the sender : "))
port = 8080
s.connect((host, port))
print("Connected ... ")

msg = s.recv(1024)
print("Host: ", msg.decode("utf-8"))
s.send(bytes("Hello World, I connected. I am your Client.", "utf-8"))
ask = s.recv(1024)
print(ask.decode("utf-8"))
username = input(str(""))
s.send(bytes(f"{username}", "utf-8"))

filename = input(str("Please enter a filename for the incoming file : "))
file = open(filename, 'wb')
file_data = s.recv(1024)
file.write(file_data)
file.close()
print("File has been received successfully.")