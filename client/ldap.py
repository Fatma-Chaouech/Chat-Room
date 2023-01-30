import ldap3
import ssl


class LDAP:
    def __init__(self, host='ldap://localhost', port=389, bind_dn='cn=Manager,dc=chatsec,dc=com', bind_password="root"):
        self.host = host
        self.port = port
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.server = ldap3.Server(host + ':' + str(port))
        self.conn = ldap3.Connection(
            self.server, user=bind_dn, password=bind_password)
        self.conn.open()
        self.conn.bind()

    def get_certificate(self, username):
        base_dn = 'cn={},dc=chatsec,dc=com'.format('cert_' + username.replace(' ', '_'))
        search_filter = '(objectClass=person)'
        self.conn.search(base_dn, search_filter, attributes=['userCertificate;binary'])

        # Retrieve the certificate information from the entry
        certificate = self.conn.response[0]['attributes']['userCertificate;binary']
        return certificate

    def disconnect(self):
        if self.conn and self.conn.bound:
            self.conn.unbind()
            self.conn.close()
            self.conn = None
