import asyncio
from json import dumps, loads
import logging
from pathlib import Path
from threading import Thread
from PIL import ImageTk, Image
import aio_pika
import aio_pika.abc
from tkinter import  Canvas, Entry, Frame, Label, PhotoImage, Tk
from ldap import LDAP
from openSSL import OpenSSLEncryption

class ChatroomPage(Frame):
    def __init__(self, window, username, certificate):
        Frame.__init__(self, window)
        self.window = self
        self.certificate = certificate
        self.canvas = self.__prepare_canvas()
        self.username = username
        self.chat_frame = self.__prepare_chat_frame()
        self.message_input = self.__prepare_input()
        self.__prepare_left_panel()
        self.__prepare_navigation_arrows()
        self.next_row = 0
        self.selected_room = None
        self.rooms = []
        self.current_listener = None
        self.room_threads = {}
        self.consumers = {}
        self.ldap = LDAP()
        self.openSSL = OpenSSLEncryption(self.ldap)
        logging.getLogger('asyncio').setLevel(logging.FATAL)


# ======================= Consumer Thread Listening ========================

    def thread_consumer(self, room_name, username):
        try:
            loop = asyncio.get_event_loop()
        except :
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        finally:
            loop.run_until_complete(
                self.listen_on_message(loop, room_name, username))
            loop.close()

    async def listen_on_message(self, loop, room_name, username):
        connection: aio_pika.RobustConnection = await aio_pika.connect_robust(
            "amqp://guest:guest@127.0.0.1/", loop=loop
        )
        async with connection:
            queue_name = (username + '.' + room_name).replace(' ', '')
            # Creating channel
            channel: aio_pika.abc.AbstractChannel = await connection.channel()

            # Declaring queue
            queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
                queue_name, durable=True
            )

            await queue.consume(self.message_callback, no_ack=True)
            print(" [*] Waiting for messages. To exit press CTRL+C")
            await asyncio.Future()
            
        

    def message_callback(self, message):
        if message.routing_key.split('.')[1] == self.selected_room.replace(' ', '') :
            message = loads(message.body)
            self.display_message(message)

# ======================= Publisher Thread Listening ========================

    def thead_publisher(self, message, room_name, queue_name: str):
        asyncio.run(self.publish(message, room_name, queue_name))
            

    async def publish(self, message, room_name, queue_name):
        connection = await aio_pika.connect("amqp://guest:guest@127.0.0.1/")
        routing_key = queue_name
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True)

            body = {
                'sender': self.username,
                'content': message,
                'room_name': room_name
            }
            # Binding queue
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=dumps(body).encode(),
                    headers={'routing_key': routing_key,
                            'certificate': self.certificate},
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=queue.name
            )
            # create the consumer thread on the room
            if queue_name == 'room_selection':
                self.current_listener = Thread(
                    target=self.thread_consumer, args=(room_name, self.username))
                self.current_listener.setDaemon(True)
                self.consumers[room_name] = self.current_listener
                self.current_listener.start()
            await connection.close()


# ======================= Main Program =========================

    def publish_message(self, _, queue_name='messaging'):
        if self.selected_room:
            if self.selected_room not in self.rooms:
                self.rooms.append(self.selected_room)
            message = self.message_input.get()
            self.openSSL.encrypt_message(message, self.certificate)
            self.message_input.delete(0, 'end')
            t = Thread(target=self.thead_publisher,
                    args=(message, self.selected_room, queue_name))
            t.start()
        else:
            print("Please select a room before sending a message.")

    def select_room(self, room_name):
        t_select = Thread(target=self.thead_publisher,
                          args=('', room_name, 'room_selection'))
        t_select.start()
        for bubble in self.chat_frame.winfo_children():
            bubble.destroy()
        self.rooms.append(room_name)
        self.selected_room = room_name

    def display_message(self, message):

        username = message['sender']
        content = message['content']
        bg_color = '#F0E68C' if username == self.username else '#D3E397'
        padx = 30 if username == self.username else 70
        anchor = 'e' if username == self.username else 'w'
        sender_label = Label(self.chat_frame, font=(
            'Arial', 10), bg='#2D2D2D', fg='white', anchor=anchor)
        sender_label.config(text=username, anchor=anchor)
        sender_label.pack(side='top', anchor=anchor, padx=padx, pady=5)
        message_bubble = Label(self.chat_frame, bg=bg_color, bd=2, relief='solid',
                               pady=10, padx=10, font=('Arial', 12), anchor=anchor, wraplength=200)
        message_bubble.config(text=content, anchor=anchor)
        message_bubble.pack(side='top', anchor=anchor, padx=padx, pady=5)
        self.next_row += 1

    def __prepare_chat_frame(self):
        chat_frame = Frame(self.window, bg='#2D2D2D')
        chat_frame.place(x=208, y=92, width=595, height=487 - 92 - 58)
        return chat_frame

    def __prepare_input(self):
        message_input = Entry(self.window, bd=2, bg='#2E2E2E', fg='white', highlightthickness=0.5,
                              insertbackground='white', width=50)
        message_input.config(highlightcolor='#93D092',
                             highlightbackground='#93D092')
        message_input.place(x=225.0, y=437.0, width=523.0, height=39.0)
        self.side_image = Image.open(relative_to_assets('button_1.png'))
        send = ImageTk.PhotoImage(self.side_image)
        label = Label(self.window, image=send, bg='green')
        label.bind("<Button-1>", self.publish_message)
        label.place(x=761.0, y=448.0, width=23.0, height=21.0)
        return message_input

    def __prepare_left_panel(self):
        self.canvas.create_rectangle(
            0.0, 5.684341886080802e-14, 208.0, 487.00000000000006, fill="#1E1E1E", outline="")
        exit_button = PhotoImage(
            file=relative_to_assets("button_2.png"))
        exit_button = Label(self.canvas, image=exit_button,
                            bg='#282727', highlightthickness=0, bd=0)
        exit_button.bind("<Button-1>", lambda event: exit())
        exit_button.place(x=22.649999618530273, y=460.04998779296875,
                          width=8.700000762939453, height=9.899993896484375)

        exit_ = Label(self.canvas, text="out", bg='#1E1E1E', fg='white', font=(
            "Inter SemiBold", 10), cursor="hand2", anchor="w")
        exit_.place(x=761.0, y=448.0, width=23.0, height=21.0)
        exit_.bind("<Button-1>", lambda event: exit())
        exit_.place(
            x=36.0,
            y=452.0,
            width=19.0,
            height=24.0
        )
        chatsec = Label(self.canvas, text="chatsec.", bg='#1E1E1E',
                        fg='#93D091', font=("Yantramanav Bold", 28), anchor="w")
        chatsec.place(x=38.0, y=51.0)

        your_chatrooms = Label(self.canvas, text="YOUR CHATROOMS", bg='#1E1E1E',
                               fg='#858282', font=("Inter SemiBold", 9), anchor="w")
        your_chatrooms.place(x=34.0, y=155.0)

        button_4 = Label(self.canvas, text="Philosophy", bg='#1E1E1E', fg='white', font=(
            "Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_4.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_4.bind("<Button-1>", lambda event,
                      room_name='Philosophy': self.select_room(room_name))
        button_4.place(
            x=34.0,
            y=192.0,
            width=125.0,
            height=14.0
        )

        button_5 = Label(self.canvas, text="News", bg='#1E1E1E', fg='white', font=(
            "Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_5.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_5.bind("<Button-1>", lambda event,
                      room_name='News': self.select_room(room_name))
        button_5.place(
            x=34.0,
            y=226.0,
            width=79.0,
            height=13.0
        )

        button_6 = Label(self.canvas, text="IT Talk", bg='#1E1E1E', fg='white', font=(
            "Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_6.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_6.bind("<Button-1>", lambda event,
                      room_name='IT Talk': self.select_room(room_name))
        button_6.place(
            x=34.0,
            y=259.0,
            width=36.0,
            height=13.0
        )

        button_7 = Label(self.canvas, text="ChatGPT", bg='#1E1E1E', fg='white', font=(
            "Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_7.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_7.bind("<Button-1>", lambda event,
                      room_name='ChatGPT': self.select_room(room_name))
        button_7.place(
            x=34.0,
            y=292.0,
            width=49.0,
            height=13.0
        )

        button_8 = Label(self.canvas, text="All About Life", bg='#1E1E1E', fg='white', font=(
            "Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_8.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_8.bind("<Button-1>", lambda event,
                      room_name='All About Life': self.select_room(room_name))
        button_8.place(
            x=34.0,
            y=325.0,
            width=125.0,
            height=13.0
        )

        button_9 = Label(self.canvas, text="Need Help", bg='#1E1E1E', fg='white', font=(
            "Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_9.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_9.bind("<Button-1>", lambda event,
                      room_name='Need Help': self.select_room(room_name))
        button_9.place(
            x=34.0,
            y=358.0,
            width=57.0,
            height=13.0
        )

    def __prepare_navigation_arrows(self):
        button_image_10 = PhotoImage(
            file=relative_to_assets("button_10.png"))
        label = Label(self.canvas, image=button_image_10,
                      bg='#282727', highlightthickness=0, bd=0)
        label.bind("<Button-1>", lambda event: print("Button 10 clicked"))
        label.place(
            x=739.75,
            y=40.75,
            width=5.5,
            height=10.5
        )

        button_image_11 = PhotoImage(
            file=relative_to_assets("button_11.png"))
        label = Label(self.canvas, image=button_image_11,
                      bg='#282727', highlightthickness=0, bd=0)
        label.bind("<Button-1>", lambda event: print("Button 11 clicked"))
        label.place(
            x=266.75,
            y=40.75,
            width=5.5,
            height=10.5
        )

    def __prepare_canvas(self):
        canvas = Canvas(self.window, bg="#272727", height=487,
                        width=803, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        return canvas

    def close_connection(self):
        exit(0)


# ========================================================================
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def prepare_window():
    window = Tk()
    window.geometry("803x487")
    window.configure(bg="#FFFFFF")
    return window
