from json import dump, dumps
from pathlib import Path
import pika
import tkinter as tk
from tkinter import END, Canvas, Entry, Frame, Label, PhotoImage, Text, Tk

class ChatroomPage(Frame):
    def __init__(self, window, controller, username):
        Frame.__init__(self, window)
        self.channel = None
        parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
        self.connection = pika.SelectConnection(parameters, self._on_connection_open, self._on_connection_closed)
        # self.connection_blocking = pika.BlockingConnection(parameters)
        # self.channel_blocking = self.connection_blocking.channel()
        self.controller = controller
        self.window = self
        self.canvas = self.__prepare_canvas()
        self.username = username
        self.chat_frame = self.__prepare_chat_frame()
        self.message_input = self.__prepare_input()
        self.__prepare_left_panel()
        self.__prepare_navigation_arrows()
        self.next_row = 0
        self.selected_room = None
        self.rooms = []
        


    def _on_connection_open(self):
        print('Connection opened')
        self.connection.channel(on_open_callback=self.on_channel_open)

    def _on_connection_closed(self, connection, reply_code, reply_text):
        print('Connection failed')
        self.connection.ioloop.stop()
        self.connection.stop()

    def on_channel_open(self, channel):
        print('Channel opened')
        self.channel = channel
        self.channel.queue_declare(queue=self.selected_room, exclusive=True)
        self.channel.basic_consume(queue=self.selected_room, on_message_callback=self.message_callback)
        
        


    def publish_message(self, _):
        if self.selected_room:
            if self.selected_room not in self.rooms:
                self.channel.queue_declare(queue=self.selected_room)
                self.rooms.append(self.selected_room)
            message = dumps({'content' : self.message_input.get(), 'sender' : self.username})
            self.message_input.delete(0, 'end')
            self.channel.basic_publish(exchange='',
                                routing_key=self.selected_room,
                                body=message)
            self.connection.ioloop.start()

        else :
            print("Please select a room before sending a message.")


    def select_room(self, room_name):
        
        for bubble in self.chat_frame.winfo_children():
            bubble.destroy()
        #if room_name not in self.rooms:
        self.rooms.append(room_name)
        self.selected_room = room_name
        # self.consume_room()
        
        

    def message_callback(self, ch, method, properties, body):
            message = body.decode()
            self.channel.basic_ack(method.delivery_tag)
            self.display_message(message)


    def display_message(self, message):
        
        print('Gonna display : ', message)
        
        username = message['sender']
        bg_color = '#F0E68C' if username == self.username else '#D3E397'
        padx = 30 if username == self.username else 70
        anchor = 'e' if username == self.username else 'w'
        message_bubble = Label(self.chat_frame, bg=bg_color, bd=2, relief='solid', pady=10, padx=10, font=('Arial', 12), anchor=anchor, wraplength=200)
        message_bubble.config(text=message['content'], anchor=anchor)
        message_bubble.pack(side='top', anchor=anchor, padx=padx, pady=5)
        self.next_row += 1


    def __prepare_chat_frame(self):
        chat_frame = Frame(self.window, bg='#2D2D2D') 
        chat_frame.place(x=208, y=92, width=595, height=487 - 92 - 58)
        return chat_frame


    def __prepare_input(self):
        message_input = Entry(self.window, bd=2, bg='#2E2E2E', fg='white', highlightthickness=0.5,
                insertbackground='white', width=50)
        message_input.config(highlightcolor='#93D092', highlightbackground='#93D092')
        message_input.place(x=225.0, y=437.0, width=523.0, height=39.0)
        send = PhotoImage(file=relative_to_assets('button_1.png'))
        label = Label(self.window, image=send, bg='#282727', highlightthickness=0, bd=0)
        label.bind("<Button-1>", self.publish_message)
        label.place(x=761.0, y=448.0, width=23.0, height=21.0)
        return message_input

    def __prepare_left_panel(self):
        self.canvas.create_rectangle(0.0, 5.684341886080802e-14, 208.0, 487.00000000000006, fill="#1E1E1E", outline="")
        exit_button = PhotoImage(
        file=relative_to_assets("button_2.png"))
        exit_button = Label(self.canvas, image=exit_button, bg='#282727', highlightthickness=0, bd=0)
        exit_button.bind("<Button-1>", lambda event: exit())
        exit_button.place(x=22.649999618530273, y=460.04998779296875, width=8.700000762939453, height=9.899993896484375)

        exit_ = Label(self.canvas, text="out", bg='#1E1E1E', fg='white', font=("Inter SemiBold", 10), cursor="hand2", anchor="w")
        exit_.place(x=761.0, y=448.0, width=23.0, height=21.0)
        exit_.bind("<Button-1>", lambda event: exit())
        exit_.place(
            x=36.0,
            y=452.0,
            width=19.0,
            height=24.0
        )
        chatsec = Label(self.canvas, text="chatsec.", bg='#1E1E1E', fg='#93D091', font=("Yantramanav Bold", 28), anchor="w")
        chatsec.place(x=38.0, y=51.0)


        your_chatrooms = Label(self.canvas, text="YOUR CHATROOMS", bg='#1E1E1E', fg='#858282', font=("Inter SemiBold", 9), anchor="w")
        your_chatrooms.place(x=34.0, y=155.0)



        button_4 = Label(self.canvas, text="Philosophy", bg='#1E1E1E', fg='white', font=("Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_4.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_4.bind("<Button-1>", lambda event, room_name='Philosophy' : self.select_room(room_name))
        button_4.place(
            x=34.0,
            y=192.0,
            width=125.0,
            height=14.0
        )


        button_5 = Label(self.canvas, text="News", bg='#1E1E1E', fg='white', font=("Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_5.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_5.bind("<Button-1>",  lambda event, room_name='News' : self.select_room(room_name))
        button_5.place(
            x=34.0,
            y=226.0,
            width=79.0,
            height=13.0
        )

        button_6 = Label(self.canvas, text="IT Talk", bg='#1E1E1E', fg='white', font=("Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_6.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_6.bind("<Button-1>", lambda event, room_name='IT Talk' : self.select_room(room_name))
        button_6.place(
            x=34.0,
            y=259.0,
            width=36.0,
            height=13.0
        )

        button_7 = Label(self.canvas, text="ChatGPT", bg='#1E1E1E', fg='white', font=("Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_7.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_7.bind("<Button-1>", lambda event, room_name='ChatGPT' : self.select_room(room_name))
        button_7.place(
            x=34.0,
            y=292.0,
            width=49.0,
            height=13.0
        )

        button_8 = Label(self.canvas, text="All About Life", bg='#1E1E1E', fg='white', font=("Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_8.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_8.bind("<Button-1>", lambda event, room_name='All About Life' : self.select_room(room_name))
        button_8.place(
            x=34.0,
            y=325.0,
            width=125.0,
            height=13.0
        )

        button_9 = Label(self.canvas, text="Need Help", bg='#1E1E1E', fg='white', font=("Inter SemiBold", 10), cursor="hand2", anchor="w")
        button_9.place(x=761.0, y=448.0, width=23.0, height=21.0)
        button_9.bind("<Button-1>", lambda event, room_name='Need Help' : self.select_room(room_name))
        button_9.place(
            x=34.0,
            y=358.0,
            width=57.0,
            height=13.0
        )
    
    def __prepare_navigation_arrows(self):
        button_image_10 = PhotoImage(
        file=relative_to_assets("button_10.png"))
        label = Label(self.canvas, image=button_image_10, bg='#282727', highlightthickness=0, bd=0)
        label.bind("<Button-1>", lambda event: print("Button 10 clicked"))
        label.place(
            x=739.75,
            y=40.75,
            width=5.5,
            height=10.5
        )

        button_image_11 = PhotoImage(
            file=relative_to_assets("button_11.png"))
        label = Label(self.canvas, image=button_image_11, bg='#282727', highlightthickness=0, bd=0)
        label.bind("<Button-1>", lambda event: print("Button 11 clicked"))
        label.place(
            x=266.75,
            y=40.75,
            width=5.5,
            height=10.5
        )
    
    def __prepare_canvas(self):
        canvas = Canvas(self.window, bg = "#272727", height = 487, width = 803, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)
        return canvas


    def close_connection(self):
        self.connection.ioloop.stop()
        self.connection.close()
        # self.connection_blocking.close()


# ========================================================================

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def prepare_window():
        window = Tk()
        window.geometry("803x487")
        window.configure(bg = "#FFFFFF")
        return window



