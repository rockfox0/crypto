import socket
from pyexpat.errors import messages

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
def rsa_encrypt(message,key):
    rsakey=RSA.importKey(key)
    cipher = PKCS1_v1_5.new(rsakey)
    cipher_text=base64.b64encode(cipher.encrypt(message.encode('utf-8')))
    return cipher_text
def main():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(('192.168.88.129',8787))
    print("连接成功")
    while True:
        try:
            messages=input("请输入你要发送的消息")
            with open('public.pem','r') as publicfile:
                public_key=publicfile.read()
            cipher_text=rsa_encrypt(messages,public_key)
            client_socket.sendall(cipher_text)#发送铭文
            reply=client_socket.recv(1024)
            print("收到回复",reply.decode('utf-8'))

        except Exception as e:
            print(f"发生异常:{e}")
            break

if __name__ == '__main__':
    main()