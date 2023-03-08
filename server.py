import socket

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.gethostname())
    print(socket.gethostbyname(socket.gethostname()))

    s.bind(('0.0.0.0', 50051))
    # s.bind(('127.0.0.1', 50008))

    # s.setblocking(0)
    s.listen(1)

    
    while True:
        # s.settimeout(0.01)
        conn, addr = s.accept()
        conn.setblocking(0)
        # conn.timeout(0.01)
        # print(conn)
        while True:
            print("wait")
            data = None
            try:
                data = conn.recv(1024)
            except socket.timeout:
                print("didint")
            if not data:
                break
            print('data : {}'.format(data))
            print( data.decode() == "none")
        # conn.close()
    s.close()

    # while True:
    #     # s.settimeout(0.01)
    #     # conn, addr = s.accept()
    #     # conn.timeout(0.01)
    #     # print(conn)
    #     while True:
    #         print("wait")
    #         data = None
    #         try:
    #             data = s.recv(1024)
    #         except socket.timeout:
    #             print("didint")
    #         if not data:
    #             break
    #         print('data : {}'.format(data))
    #     # conn.close()
    # s.close()