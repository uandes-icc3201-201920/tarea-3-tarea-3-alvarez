import socket
from _thread import *
import threading
import random

database = {}
print_lock = threading.Lock()
rng_key = random.randint(1000, 10000)

def threaded(c):
    print('New Thread')
    global rng_key
    while True:
        data_str = ''
        data = c.recv(1024)
        data_str += str(data.decode('ascii'))
        print(data_str)
        if not data:
            print('Bye')
            break
        message = '01 BAD REQUEST'
        command_array = data_str.split("(")
        command = command_array[0]
        if "insert" == command:
            print_lock.acquire()
            value = data_str.split("'")
            data_str = data_str.replace("(", ",")
            key = data_str.split(",")
            if key[1]:
                if key[1] in database:
                    message = '03 KEY TAKEN'
                else:
                    print("insert " + value[1] + " into " + key[1])
                    database[key[1]] = value[1]
                    message = '20 INSERTED'
            else:
                rng_key = rng_key
                print("insert " + value[1] + " into " + str(rng_key))
                database[str(rng_key)] = value[1]
                message = '20 INSERTED, KEY=' + str(rng_key)
                rng_key += 1
            print_lock.release()
        elif "get" == command:
            data_str = data_str.replace("(", ",")
            key = data_str.split(",")
            if key[1] in database:
                print("get " + key[1])
                message = '30 GOT, VALUE=' + database[key[1]]
            else:
                message = '02 KEY NOT FOUND'
        elif "peek" == command:
            data_str = data_str.replace("(", ",")
            key = data_str.split(",")
            print("peek " + key[1])
            if key[1] in database:
                message = '40 PEEKED, VALUE=True'
            else:
                message = '40 PEEKED, VALUE=False'
        elif "update" == command:
            print_lock.acquire()
            value = data_str.split("'")
            data_str = data_str.replace("(", ",")
            key = data_str.split(",")
            print("update " + key[1] + " to " + value[1])
            if key[1] in database:
                database[key[1]] = value[1]
                message = '50 UPDATED'
            else:
                message = '02 KEY NOT FOUND'
            print_lock.release()
        elif "delete" == command:
            print_lock.acquire()
            data_str = data_str.replace("(", ",")
            key = data_str.split(",")
            if key[1] in database:
                print("delete " + key[1])
                del database[key[1]]
                message = '60 DELETED'
            else:
                message = '02 KEY NOT FOUND'
            print_lock.release()
        elif "list" == command:
            print("list")
            message = '60 LIST'
            for key in database.keys():
                message += '\n' + str(key)
        elif "handshake" == command:
            message = '10 CONNECTED'
        else:
            message = '01 BAD REQUEST'
        print(data_str)
        c.send(message.encode('ascii'))
    c.close()


def Main():
    host = ""
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    s.listen(5)
    print("socket is listening")

    while True:
        c, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (c,))
    s.close()

if __name__ == '__main__':
    Main()