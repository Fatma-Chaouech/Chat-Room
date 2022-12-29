import time 

class Message:
    def __init__(self, chatroom, content):
        self.chatroom = chatroom
        self.content = content
        self.timestamp = time.time()

    def __str__(self):
        return '[{}] {}: {}'.format(self.timestamp, self.chatroom.name, self.content)