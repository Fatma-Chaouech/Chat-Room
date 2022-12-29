import socket
import ssl
import subprocess

class OpenSSLClient:
    def __init__(self, CA, user, certs_path, keys_path):
        self.CA = CA
        self.user = user
        self.tls_certificate = None
        self.certs_path = certs_path + '/' + user.name + '.pem'
        self.keys_path = keys_path + '/' + user.name + '.pem'

    def __create_csr(self, csr_path):
        subprocess.run([
            self.openssl_path, 'req', '-new', '-out', csr_path, '-keyout', self.certs_path,
            '-subj', '/C={}/ST={}/O={}/OU={}/CN={}/emailAddress={}'.format(self.user.country, self.user.state, self.user.organization, self.user.organizational_unit, self.user.common_name, self.user.email_address)
        ])
    
    def __generate_tls_certificate(self, csr_path):
        # Generate a new TLS certificate by first generating a CSR, then signing it using the CA's private key
        csr = self.__create_csr(csr_path)
        return self.CA.sign_csr(csr)
    
    def verify_certificate(self, csr_path):
        if not self.tls_certificate:
            self.tls_certificate = self.__generate_tls_certificate(csr_path)
        return self.CA.verify_certificate(self.tls_certificate)

    def __create_ssl_context(self):
        # Create an SSL context object and configure it to use the CA's certificate, the client's certificate and private key,
        # and the required SSL/TLS protocols and cipher suites
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_verify_locations(self.CA.ca_cert_path)
        ssl_context.load_cert_chain(self.certs_path, self.keys_path)
        ssl_context.set_ciphers("HIGH:!MD5")
        return ssl_context
    
    def create_secure_client_socket(self, host, port):
        # Create a TCP socket and then wrap it in an SSL/TLS layer using the SSL context created earlier
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_hostname = host + ':' + str(port)
        ssl_context = self.__create_ssl_context()
        return ssl_context.wrap_socket(client_socket, ca_certs=self.CA.ca_cert_path, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLS, ciphers=None, server_hostname=server_hostname)
