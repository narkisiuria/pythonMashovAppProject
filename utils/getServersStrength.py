import threading
import socket

target = "127.0.0.1"
port = 9999

def attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("connecting to server")
            s.connect((target, port))
            print("successfuly connected to server")
            print("sending packet")
            s.sendall(f"get_schedule|{"ט'6"}".encode('utf-8'))
            print("packet sent")
            print("dissconnecting ")
            s.close()
            print("successfuly dissconnected")
        except:
            pass


for i in range(100):
    thread = threading.Thread(target=attack)
    thread.start()