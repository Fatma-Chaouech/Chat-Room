import pika

class RabbitMq():
    def __init__(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="login")
        self.channel.queue_purge(queue='login')
        self.channel.queue_declare(queue="messaging", durable=True)
        self.channel.queue_purge(queue='messaging')
        self.channel.queue_declare(queue="room_selection", durable=True)
        self.channel.queue_purge(queue='room_selection')

                            
    def add_queue(self, name):
        # Use this to create a queue for every chatroom
        self.channel.queue_declare(queue=name)
    

    def send_message(self, message, name):
        # Use this to send a message to a chatroom
        self.channel.basic_publish(exchange='',
                    routing_key=name,
                    body=message)
    

    def close_connection(self):
        self.connection.close()

