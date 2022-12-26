import socket
import ssl
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
    
    def generate_tls_certificate(self, cn, email):
        # Generate a new TLS certificate by first generating a CSR, then signing it using the CA's private key
        csr = self.create_csr(cn, email)
        tls_certificate = self.sign_csr(csr)
        return tls_certificate
    
    def verify_certificate(self, certificate):
        # Verify the certificate using the CA's certificate
        try:
            ssl.verify_certificate_chain(certificate, self.ca_certs_path)
        except ssl.SSLError:
            return False
        return True


    def create_ssl_context(self):
        # Create an SSL context object and configure it to use the CA's certificate, the client's certificate and private key,
        # and the required SSL/TLS protocols and cipher suites
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_verify_locations(self.ca_cert_path)
        ssl_context.load_cert_chain(self.client_cert_path, self.client_key_path)
        ssl_context.set_ciphers("HIGH:!MD5")
        return ssl_context
    
    def wrap_socket(self, socket, hostname):
        return ssl.wrap_socket(socket, ca_certs=self.ca_certs_path, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLS, ciphers=None, server_hostname=hostname)

    def create_secure_client_socket(self, host, port):
        # Create a TCP socket and then wrap it in an SSL/TLS layer using the SSL context created earlier
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_hostname = host + ':' + str(port)
        return self.ssl_context.wrap_socket(client_socket, server_hostname=server_hostname)
