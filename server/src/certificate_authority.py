import ssl
import subprocess


class CertificateAuthority:
    def __init__(self, openssl_path, ca_cert_path, ca_key_path, hostname):
        self.openssl_path = openssl_path
        self.ca_cert_path = ca_cert_path
        self.ca_key_path = ca_key_path
        self.hostname = hostname
    
    def sign_csr(self, csr_path, certs_path):
        print('Signing the CSR request...')
        subprocess.run([
            self.openssl_path, 'x509', '-req', '-in', csr_path, '-passin', 'pass:secret', '-out', certs_path,
            '-CA', self.ca_cert_path, '-CAkey', self.ca_key_path, '-CAcreateserial', '-days', '365'
        ])
        with open(certs_path, 'rb') as f:
            signed_certificate = f.read()
        return signed_certificate
        