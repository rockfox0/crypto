from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
def generate():
    rsa=RSA.generate(3072)
    private_pem=rsa.exportKey()
    with open("private.pem","wb") as f:
        f.write(private_pem)#导出为PEM格式
    public_pem=rsa.publickey().exportKey()
    with open("public.pem","wb") as f:
        f.write(public_pem)
generate()