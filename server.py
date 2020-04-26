import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8080
s.bind((host, port))
s.listen(2)
print(host)
print("Waiting for any incoming connections ... ")
conn, addr = '', ''
launch = False
while not launch:
    conn, addr = s.accept()
    print(addr, "Has connected to the server")
    conn.send(bytes("Welcome to the server", "utf-8"))
    ans = conn.recv(1024)
    str_ans = ans.decode("utf-8")
    print(addr, ": ", str_ans)
    code = conn.recv(8)
    str_code = code.decode("utf-8")
    if str_code == "Code0001":
        conn.send(bytes("Be ready!", "utf-8"))
        conn.send(bytes("Code0000", "utf-8"))
        files = conn.recv(1024)
        launch = True
        print(launch)


print(addr, " is Service_Announcer")
ready = True
# print(ready)

while ready:
    try:
        print("Waiting for any incoming connections ... ")
        client, address = s.accept()
        print(address, "Has connected to the server")
        client.send(bytes("Welcome to the server", "utf-8"))
        ans = client.recv(1024)
        str_ans = ans.decode("utf-8")
        print(address, ": ", str_ans)
        conn.send(bytes(f"{address}", "utf-8"))
        alert = conn.recv(1024)
        str_alert = alert.decode("utf-8")
        print("Announcer: ", str_alert)
        client.send(bytes(f"Announcer: {str_alert}", "utf-8"))
        user_name = client.recv(1024)
        str_user_name = user_name.decode("utf-8")
        print(address, ": My user name is ", str_user_name)
        conn.send(bytes(f"{str_user_name}", "utf-8"))
        ready_toFT = True
        print(ready_toFT)
        if ready_toFT:
            filename = input(str("Enter the file's name you want to send: "))
            file = open(filename, 'rb')
            file_data = file.read(1024)
            client.send(bytes(file_data))
            print(f"File {filename} is sent to user {str_user_name} at {time.asctime()}.")
            conn.send(bytes(f"{filename}", "utf-8"))
    except Exception as e:
        print(str(e))
        pass
