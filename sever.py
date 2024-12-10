import socket
import threading
def handle_client(client_socket):
    while True:
        try:
            data=client_socket.recv(1024)
            if not data:
                break
            print(f"收到的:{data.decode('utf-8')}")
            reply=input("I have know it And Say:")
            client_socket.send(reply.encode('utf-8'))
        except Exception as e:
            print(f"发生异常:{e}")
    client_socket.close()
def main():
    sever_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sever_socket.bind(('192.168.88.129',8181))
    sever_socket.listen(5)
    print("等待连...")
    while True:
        client_socket,client_address=sever_socket.accept()
        print(f"连接from：{client_address}")
        client_handler=threading.Thread(target=handle_client,args=(client_socket,))
        client_handler.start()
if __name__=="__main__":
    main()


