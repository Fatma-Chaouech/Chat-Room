import time 

class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
        self.timestamp = time.time()

    def __str__(self):
        return '[{}] {}: {}'.format(self.timestamp, self.sender, self.content)