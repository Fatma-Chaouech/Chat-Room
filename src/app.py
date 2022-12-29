import sys
sys.path.insert(0,'./src')
from message import Message
import threading
import time
from room import Room
from user import User

class ChatRoomApp:
    def __init__(self, ldap_client, chatroom_keys_path, certs_path, keys_path):
        self.ldap_client = ldap_client
        self.chat_rooms = {}
        self.users = {}
        self.certs_path = certs_path
        self.keys_path = keys_path
        self.chatroom_keys_path = chatroom_keys_path
        self.lock = threading.Lock()
        self.ldap_client.connect()

    def add_chat_room(self, chat_name):
        chat_room = Room(chat_name, self.chatroom_keys_path)
        with self.lock:
            self.chat_rooms[chat_name] = chat_room

    def remove_chat_room(self, chat_name):
        with self.lock:
            self.chat_rooms.pop(chat_name)

    def get_chat_room(self, chat_name):
        with self.lock:
            if chat_name in self.chat_rooms.keys():
                return self.chat_rooms[chat_name]
            return None

    def get_chat_rooms(self):
            with self.lock:
                return self.chat_rooms

    def add_user(self, user):
        with self.lock:
            if user.name in self.users:
                raise Exception('User already exists')
            else : 
                self.ldap_client.add_user(user)
                self.users[user.name] = user

    def remove_user(self, name):
        with self.lock:
            if name not in self.users.keys():
                raise Exception('User does not exist')
            else : 
                self.ldap_client.remove_user(name)
                self.users.pop(name)

    def get_user(self, name):
        with self.lock:
            return self.users.get(name)

    def welcome(self):
        print('Welcome to the chatroom app!')
        while True:
            # Display sign up or login options
            print("1. Sign up")
            print("2. Login")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                # Prompt the user for their sign up details and add them to the LDAP server
                print("Sign up")
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                new_user = User(self.CA, self.ldap_client, username, username.lower(), self.certs_path, self.keys_path, organizational_unit=username+"OrgUnit", organization=username+"Org", state=username+"-State", country=username+"-Country", email_address=username+"@gmail.com", common_name=username)
                self.add_user(new_user)
                print("Sign up successful!")
                self.start()
                self.ldap_client.disconnect()
            elif choice == "2":
                # Prompt the user for their login details and verify them against the LDAP server
                print("Login")
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if self.ldap_client.verify_login(username, password):
                    print("Login successful!")
                    # Once the user has logged in, allow them to send messages and join rooms
                    self.start()
                    self.ldap_client.disconnect()
                else:
                    print("Invalid login details.")
            else:
                print("Invalid choice.")

    def start(self):
        # Start the messaging thread for each user
        for user in self.users.values():
            user_thread = threading.Thread(target=self.message_thread, args=(user,))
            user_thread.start()

        # Run the chatroom app main loop
        while True:
            # Display a list of available chat rooms
            print('Available chat rooms:')
            for i, chat_name in enumerate(self.chat_rooms):
                print('{}: {}'.format(i, chat_name))

            # Prompt the user to select a chat room
            chat_name = input('Where do you want to enter?')
            # Check if the user has chosen to quit the chatroom app
            if chat_name == 'q':
                break
    
            # Get the selected chat room
            try:
                selected_chat_room = self.chat_rooms[chat_name]
            except (ValueError, IndexError):
                print('Invalid chat room selection.')
                continue
    
            # Join the selected chat room
            selected_chat_room.join()
            while True : 
                # Prompt the user to send a message
                content = input('Enter your message (q to quit): ')
                message = Message(selected_chat_room, content)
                if message == 'q':
                    break
                # Send the message to the chat room
                selected_chat_room.send_message(message)
    
            # Leave the chat room when the user is done
            selected_chat_room.leave()
		
    def message_thread(self, user):
        while True:
            # Check for new messages for the user
            new_messages = user.get_messages()
    
            # Display the new messages
            for message in new_messages:
                print(message.content)
    
            # Sleep for a short period of time before checking for new messages again
            time.sleep(0.1)