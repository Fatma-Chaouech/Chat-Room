from OpenSSL import crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class OpenSSLEncryption :
    def __init__(self, ldap):
        self.ldap = ldap


    def encrypt_message(self, message, certificate):
        with open(certificate, "rb") as cert_file:
            cert_data = cert_file.read()
            pub_key = RSA.import_key(cert_data)
            cipher = PKCS1_OAEP.new(pub_key)
            encrypted_message = cipher.encrypt(message.encode())
        return encrypted_message