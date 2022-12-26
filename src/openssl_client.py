import subprocess

class OpenSSLClient:
    def __init__(self, openssl_path, ca_cert_path, ca_key_path):
        self.openssl_path = openssl_path
        self.ca_cert_path = ca_cert_path
        self.ca_key_path = ca_key_path

    def create_csr(self, csr_path, common_name, email_address, country, state, organization, organizational_unit):
        subprocess.run([
            self.openssl_path, 'req', '-new', '-out', csr_path, '-keyout', csr_path,
            '-subj', '/C={}/ST={}/O={}/OU={}/CN={}/emailAddress={}'.format(country, state, organization, organizational_unit, common_name, email_address)
        ])

    def sign_csr(self, csr_path, cert_path):
        subprocess.run([
            self.openssl_path, 'x509', '-req', '-in', csr_path, '-out', cert_path,
            '-CA', self.ca_cert_path, '-CAkey', self.ca_key_path, '-CAcreateserial', '-days', '365'
        ])