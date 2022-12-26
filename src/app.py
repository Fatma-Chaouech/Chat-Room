import threading
import time

class ChatRoomApp:
    def __init__(self, ldap_client, openssl_client, chat_rooms=[]):
        self.ldap_client = ldap_client
        self.openssl_client = openssl_client
        self.chat_rooms = chat_rooms
        self.users = {}
        self.lock = threading.Lock()

    def add_user(self, user):
        with self.lock:
            self.users[user.name] = user

    def remove_user(self, user):
        with self.lock:
            self.users.pop(user.name)

    def add_chat_room(self, chat_room):
        with self.lock:
            self.chat_rooms.append(chat_room)

    def remove_chat_room(self, chat_room):
        with self.lock:
            self.chat_rooms.remove(chat_room)

    def get_chat_room(self, name):
        with self.lock:
            for chat_room in self.chat_rooms:
                if chat_room.name == name:
                    return chat_room
            return None

    def get_user(self, name):
        with self.lock:
            return self.users.get(name)

    def get_chat_rooms(self):
        with self.lock:
            return self.chat_rooms

    def run(self):
        # Start the messaging thread for each user
        for user in self.users.values():
            user_thread = threading.Thread(target=self.message_thread, args=(user,))
            user_thread.start()

        # Run the chatroom app main loop
        while True:
            # Display a list of available chat rooms
            print('Available chat rooms:')
            for i, chat_room in enumerate(self.chat_rooms):
                print('{}: {}'.format(i, chat_room.name))

            # Prompt the user to select a chat room
            selected_index = input('Enter the index')
						# Check if the user has chosen to quit the chatroom app
            if selected_index == 'q':
                break
    
            # Get the selected chat room
            try:
                selected_index = int(selected_index)
                selected_chat_room = self.chat_rooms[selected_index]
            except (ValueError, IndexError):
                print('Invalid chat room selection.')
                continue
    
            # Join the selected chat room
            selected_chat_room.join()
    
            # Leave the chat room when the user is done
            selected_chat_room.leave()
		
    def message_thread(self, user):
        while True:
            # Check for new messages for the user
            new_messages = user.get_new_messages()
    
            # Display the new messages
            for message in new_messages:
                print(message)
    
            # Sleep for a short period of time before checking for new messages again
            time.sleep(0.1)