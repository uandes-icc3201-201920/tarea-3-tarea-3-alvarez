import socket


def Main():
    global s
    host = input('Insert server IP: ')
    port = int(input('Insert server port: '))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        message = "bad()"
        command = input('\nInsert command: ')
        if command == 'connect':
            host = input('Insert server IP: ')
            port = int(input('Insert server port: '))
            message = "handshake()"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
        elif command == 'disconnect':
            s.close()
            break
        elif command == 'insert':
            value = input('Insert value: ')
            key = input('Insert integer key (leave blank for next key): ')
            if key.isdigit():
                print("User input is Number ")
                message = "insert(" + key + ",'" + value + "')"
            else:
                print("User input is blank ")
                message = "insert(" + ",'" + value + "')"
        elif command == 'get':
            key = input('Insert key: ')
            message = "get(" + key + ")"
        elif command == 'peek':
            key = input('Insert key: ')
            message = "peek(" + key + ")"
        elif command == 'update':
            value = input('Insert value: ')
            key = input('Insert key: ')
            message = "update(" + key + ",'" + value + "')"
        elif command == 'delete':
            key = input('Insert key: ')
            message = "delete(" + key + ")"
        elif command == 'list':
            message = "list"

        code = message.encode('ascii')
        s.send(code)
        data = s.recv(1024)
        print('Received from the server :', str(data.decode('ascii')))



if __name__ == '__main__':
    Main()