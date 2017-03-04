import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

def byte2carray(data, n=16):
	t = ""
	for chunk in [data[i:i + n] for i in xrange(0, len(data), n)]:
		t += '"'
		for c in chunk:
			t+='\\x'+c.encode('hex')
		t += '"\r\n'
	return t[:-2]
	
def byte2intarray(data):
	t = "{"
	for c in data:
		t+=str(int(c.encode('hex'), 16)) + ', '
	t += ',0 };'
	return t

class AESCipher(object):

    def __init__(self, key): 
        self.bs = 16
        self.key = key
        #self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(raw)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self._unpad(cipher.decrypt(enc)).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
	