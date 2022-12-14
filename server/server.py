import ldap

# Set up the LDAP server and client certificates and keys
project_path = "C:/Users/Fatma/OneDrive/Desktop/Chat-Room"
server_cert = project_path + "/server/signed_certificate.pem"
server_key = project_path + "/server/private_key.pem"
client_cert = "/path/to/client.crt"
client_key = "/path/to/client.key"

# Connect to the LDAP server and start TLS
ldap_handle = ldap.initialize("ldaps://ldap.example.com")
ldap_handle.set_option(ldap.OPT_X_TLS_CACERTFILE, project_path + "/root/ca.crt")
ldap_handle.set_option(ldap.OPT_X_TLS_CERTFILE, server_cert)
ldap_handle.set_option(ldap.OPT_X_TLS_KEYFILE, server_key)
ldap_handle.start_tls_s()

# Bind to the LDAP server using the DN and password of the client
ldap_handle.simple_bind_s("cn=client,dc=chatsec,dc=com", "clientpass")

# Perform LDAP operations as needed...

# Close the LDAP connection
ldap_handle.unbind_s()
