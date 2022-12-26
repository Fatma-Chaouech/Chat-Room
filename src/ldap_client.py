import ldap3
import ssl

class LDAPClient:
    def __init__(self, host, port, ca_cert_path, bind_dn, bind_password):
        self.host = host
        self.port = port
        self.ca_cert_path = ca_cert_path
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.conn = None

    def connect(self):
        # Create a TLS context with the CA certificate
        tls_ctx = ssl.create_default_context(cafile=self.ca_cert_path)

        # Connect to the LDAP server
        server = ldap3.Server(self.host, port=self.port, use_ssl=True, tls=tls_ctx)
        self.conn = ldap3.Connection(server, user=self.bind_dn, password=self.bind_password)

        # Bind to the LDAP server
        if not self.conn.bind():
            raise Exception('LDAP bind failed: {}'.format(self.conn.result))

    def disconnect(self):
        self.conn.unbind()

    def add_user(self, dn, attrs):
        if not self.conn.add(dn, attributes=attrs):
            raise Exception('LDAP add failed: {}'.format(self.conn.result))

    def delete_user(self, dn):
        if not self.conn.delete(dn):
            raise Exception('LDAP delete failed: {}'.format(self.conn.result))

    def search_user(self, dn, filter, attributes):
        if not self.conn.search(dn, filter, attributes=attributes):
            raise Exception('LDAP search failed: {}'.format(self.conn.result))
        return self.conn.entries