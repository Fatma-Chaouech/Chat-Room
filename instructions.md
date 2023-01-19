# General Step

1. Install and setup OpenLDAP server.
2. Create a PKI infrastrusture.
3. Install RabbitMQ and run it.
4. Run the server code
5. Run the client code

# Setup OpenLDAP

## OpenLDAP

Allows to store user information, such as passwords and public keys, in a centralized directory.

## Steps

1. Edit the configuration files (under C:\OpenLDAP) such as slapd.conf or cn=config. 
    1. Edit the slapd.conf or slapd.d configuration file: The slapd.conf file (or the slapd.d directory in newer versions of OpenLDAP) contains the main configuration options for the OpenLDAP server. You will need to edit this file to specify various options such as the server's domain name, database backend, and security settings.
    2. Set the server's domain name: You will need to specify the domain name of the server in the suffix option in the slapd.conf file. This should be the base DN (Distinguished Name) of the directory tree that the server will manage.
    3. Choose a database backend: OpenLDAP supports several different types of database backends, such as Berkeley DB and MDB. You will need to choose a backend and specify it in the database option in the slapd.conf file. You will also need to configure any additional options for the chosen backend.
    4. Configure security options: You will need to specify the security options for the server, such as whether to use TLS (Transport Layer Security) or SASL (Simple Authentication and Security Layer) for authentication. You can also specify the certificate file to use for TLS, as well as any other security-related options.
        
        ```bash
        ## IN slapd.conf
        # Require TLS for all LDAP operations
        security tls=yes
        
        # Require clients to authenticate using a certificate
        security ssf=128
        
        # Require clients to authenticate using a strong password
        # The value of "ssf" should be set to at least 128
        security ssf=128
        ```
        
    5. Configure access controls: You will need to specify the access controls for the server by creating access control lists (ACLs) in the slapd.conf file. These ACLs specify who is allowed to access the directory and what they are allowed to do.
2. Create LDAP database.
    
    ```bash
    Tools : ldapadd _ ldapmodify
    ```
    
3. Define the structure of tha database, including the object classes and attributes that will be used.
4. Add the users, groups and other objects.
    
    ```bash
    Tools : ldapadd _ ldapmodify
    ```
    
5. Test the server.
    1. Run the server
        1. Go to run directory under C:/OpenLDAP
        2. run
    
      b.  Send request

    ```bash
    ldapsearch -h chatsec://server1 -p 389 -D "cn=Manager,dc=chatsec,dc=com" -w secret -b "dc=chatsec,dc=com" -s sub "(objectClass=*)”
    ```
# Create PKI Infrastructure

## Steps

1. Install Openssl
2. Create root certificate authority (CA) : Generate root CA certificate and private key
    
    ```bash
    openssl req -new -x509 -days 3650 -extensions v3_ca -keyout root/ca.key -out root/ca.crt
    ```
    
    <aside>
    
    - openssl req: This command is used to generate a certificate signing request (CSR) or a self-signed certificate. In this case, we are using it to generate a self-signed certificate.
    - new: This option specifies that a new certificate and key should be generated.
    - x509: This option specifies that the output should be a self-signed certificate rather than a CSR.
    - days 3650: This option specifies the number of days that the certificate should be valid for.
    - extensions v3_ca: This option specifies that the certificate should be a version 3 CA certificate.
    - keyout private/ca.key: This option specifies the file in which the private key should be stored.
    - out certs/ca.crt: This option specifies the file in which the certificate should be stored.
    </aside>
    
3. Generate a private key for a server
    
    ```bash
    openssl genrsa -aes256 -out server/private_key.pem 2048
    ```
    
    <aside>
    
    Using the -aes256 option when generating a private key has the following benefits :
    
    - It adds an extra layer of security to the private key, by encrypting it with a strong encryption algorithm.
    - It requires a password to be specified, which must be provided in order to use the private key. This can help prevent unauthorized access to the private key.
    </aside>
    
4. Create a certificate signing request (CSR) to the CA.
    
    ```bash
    openssl req -new -key server/private_key.pem -out server/csr.pem
    ```
    
5. Use the CA to sign the request