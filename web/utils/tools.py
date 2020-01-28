import base64
import socket
from web.settings import sys_aes_key, sys_aes_iv
from Crypto.Cipher import AES


def machine_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    try:
        return s.getsockname()[0]
    finally:
        s.close()


class AesCrypto:
    def __init__(self, key, IV):
        self.key = key
        self.iv = IV
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        crypto = AES.new(self.key, self.mode, self.iv)
        length = 16
        def pad(s): return s + ((length - len(s) % length)
                                * chr(length - len(s) % length)).encode()
        r = crypto.encrypt(pad(text))
        return base64.b64encode(r)

    def decrypt(self, text):
        text = base64.b64decode(text)
        def unpad(s): return s[0:-s[-1]]
        crypto = AES.new(self.key, self.mode, self.iv)
        plain_text = unpad(crypto.decrypt(text)).decode()
        return plain_text


aes_tools = AesCrypto(key=sys_aes_key, IV=sys_aes_iv)
