# ChatSec : A secure Chat-Room

## Description

This is a real-time chatroom application that uses RabbitMQ for communication between clients and the server.

## Features

- Real-time messaging between clients using RabbitMQ
- User authentication and authorization using OpenLDAP
- SSL/TLS encryption for secure communication

## Requirements

Make sure you have the necessary software installed on your system :

- Python 3.x
- OpenSSL
- OpenLDAP
- RabbitMQ

## Steps

1. Clone the repository:

```bash
git clone <https://github.com/yourusername/chatroom-app.git>
```

1. Configure the LDAP server (for more information, check out [instructions.md](https://github.com/Fatma-Chaouech/Chat-Room/blob/main/server/instructions.md))
2. Run the LDAP server :
    
    ```bash
    # In openLDAP's directory
    slapd -d 1 -h "ldap://localhost:389" -f .\\slapd.conf
    Run the RabbitMQ server
    ```
    
3. Create a PKI infrastructure (check [instructions.md](https://github.com/Fatma-Chaouech/Chat-Room/blob/main/server/instructions.md) for more information)
4. Run the RabbitMQ server
5. Run the server [run.py](https://github.com/Fatma-Chaouech/Chat-Room/blob/main/server/run.py) file
6. Run the client’s [run.py](https://github.com/Fatma-Chaouech/Chat-Room/blob/main/client/run.py) file
7. Have fun!

## Contributing

This project is open to contributions. If you find any bugs or have any suggestions for new features, please open an issue or a pull request.

## References

[LDAP](https://soshace.com/integrate-ldap-authentication-with-flask/)

[PKI](https://www.geeksforgeeks.org/public-key-infrastructure/)

[Openldap Server Configuration](https://computingforgeeks.com/install-and-configure-openldap-server-ubuntu/)