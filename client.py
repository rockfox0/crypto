import socket
def main():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(('192.168.88.129',8181))
    print("连接成功")
    while True:
        try:
            message = input("You want to say :")
            client_socket.send(message.encode('utf-8'))
            reply=client_socket.recv(1024)
            print("收到回:",reply.decode('utf-8'))
        except Exception as e:
            print(f"wrongL{e}")
            break
    client_socket.close()
if __name__ == '__main__':
    main()