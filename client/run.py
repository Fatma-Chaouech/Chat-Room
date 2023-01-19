import json
from pathlib import Path
from tkinter import *
from PIL import ImageTk, Image
import pika

from chatroom_page import ChatroomPage



class LoginPage(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("803x487")
        self.resizable(False, False)
        self.window = Frame(self)
        self.title("Login")
        self.frames = {}
        self.username = None
        parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="login")
        self.canvas = self.__prepare_canvas()
        self.window.pack(side="top", fill="both", expand=True)
        
        # ========================================================================
        # ============ Logo ================================================
        # ========================================================================
        self.side_image = Image.open(relative_to_assets('logo.png'))
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.window, image=photo, bg='#272727')
        self.side_image_label.image = photo
        self.side_image_label.place(x=250, y=20)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.window, text="Sign Up", bg="#272727", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=340, y=150)

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        self.username_label = Label(self.window, text="Username", bg="#272727", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=270, y=200)
        self.username_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#272727", fg="#6b6a69", font=("yu gothic ui ", 12, "bold"))
        self.username_entry.place(x=300, y=235, width=270)
        self.username_line = Canvas(self.window, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=270, y=259)

        # ===== Username icon =========
        self.username_icon = Image.open(relative_to_assets('username_icon.png'))
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.window, image=photo, bg='#272727')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=270, y=232)

        # ========================================================================
        # ============================password====================================
        # ========================================================================
        self.password_label = Label(self.window, text="Password", bg="#272727", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=270, y=280)
        self.password_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#272727", fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show="*")
        self.password_entry.place(x=300, y=316, width=244)
        self.password_line = Canvas(self.window, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=270, y=340)

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        self.lgn_button = Image.open(relative_to_assets('btn.png'))
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.window, image=photo, bg='#93D092' )
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=270, y=380)
        self.login_ = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0, bg='#93D092', cursor='hand2', activebackground='#93D092', fg='white')
        self.login_.bind("<Button-1>", self.__login)
        self.login_.place(x=20, y=10)

        # ======== Password icon ================
        self.password_icon = Image.open(relative_to_assets('password_icon.png'))
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.window, image=photo, bg='#272727')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=270, y=314)

        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage(file=relative_to_assets('show.png'))
        self.hide_image = ImageTk.PhotoImage(file=relative_to_assets('hide.png'))
        self.show_button = Button(self.window, image=self.show_image, relief=FLAT,
                                activebackground="#272727", borderwidth=0, background="#272727", cursor="hand2")
        self.show_button.bind("<Button-1>", self.show)
        self.show_button.place(x=550, y=314)


    def show(self, _):
        self.hide_button = Button(self.window, image=self.hide_image,relief=FLAT,
                                activebackground="#272727", borderwidth=0, background="#272727", cursor="hand2")
        self.hide_button.bind("<Button-1>", self.hide)
        self.hide_button.place(x=550, y=314)
        self.password_entry.config(show='')

    def hide(self, _):
        self.show_button = Button(self.window, image=self.show_image, relief=FLAT,
                                activebackground="#272727", borderwidth=0, background="#272727", cursor="hand2")
        self.show_button.bind("<Button-1>", self.show)
        self.show_button.place(x=550, y=314)
        self.password_entry.config(show='*')


    def __login(self, _): 
        username = self.username_entry.get()
        password = self.password_entry.get()
        body = {
            'username': username,
            'password': password
        }
        self.frames[ChatroomPage] = ChatroomPage(self.window, self, username) 
        self.channel.basic_publish(exchange='',
                            routing_key='login',
                            body=json.dumps(body))
        self.username = username
        self.channel.queue_declare(queue=username)
        self.channel.basic_consume(queue=username, on_message_callback=self.login_callback)
        self.channel.start_consuming()
        
    
    def __prepare_canvas(self):
        canvas = Canvas(self.window, bg = "#272727", height = 487, width = 803, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)
        return canvas

    def show_frame(self):
        self.connection.close()
        frame = self.frames[ChatroomPage]
        frame.pack(side="top", fill="both", expand=True)
        frame.tkraise()
    
    def login_callback(self, ch, method, properties, body):
        self.channel.stop_consuming()
        response = json.loads(body.decode())
        print(response)
        if response['status'] == 'success':
            self.show_frame()
        elif response['status'] == 'error':
            print(response['message'])

        
# ========================================================================

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



def run():
    main = LoginPage()
    main.mainloop()

run()