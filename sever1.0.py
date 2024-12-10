import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
def rsa_decrypt(cipher_text,key):
    rsakey=RSA.importKey(key)
    cipher=PKCS1_v1_5.new(rsakey)
    text=cipher.decrypt(base64.b64decode(cipher_text),rsakey)
    return text
def handle_client(client_socket):
    while True:
        try:
            data=client_socket.recv(1024)
            if not data:
                   break
            keypath='private.pem'
            with open(keypath,'r',encoding='utf-8') as privatefile:
                 privatekey=privatefile.read()
            decode_data=data.decode('utf-8')#对收到数据解码
            plaintext=rsa_decrypt(data,privatekey)
            print(f"收到消息:{plaintext}")
            reply="收到消息"
            client_socket.sendall(reply.encode('utf-8'))
        except Exception as e:
            print(f"发生异常:{e}")
            break

def main():
    sever_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sever_socket.bind(('192.168.47.152',8787))
    sever_socket.listen(5)
    print("等待连接...")

    while True:
        client_socket,client_address=sever_socket.accept()
        print(f"连接来自:{client_address}")
        client_handler=threading.Thread(target=handle_client,args=(client_socket,))
        client_handler.start()
if __name__ == '__main__':
    main()
