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
        # conn.setblocking(0)
        
        while True:
            # print("wait")
            try:
                data = conn.recv(1024)
                print('data : {}'.format(data))
                # print( data.decode() == "none")
            except BlockingIOError:
                pass
        
        conn.close()
    s.close()
