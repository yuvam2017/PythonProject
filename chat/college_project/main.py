import socket
from threading import Thread
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, SlideTransition, ScreenManager
from kivy.clock import Clock
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.animation import Animation

class ScreenManager(ScreenManager): pass

class HomeScreen(Screen): pass

class CreateRoom(Screen): pass

class JoinRoom(Screen): pass

class ChatRoom(Screen): pass

class ChatApp(MDApp):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	room_id = ""
	name = ""

	def __init__(self, **kwargs):
		super(ChatApp, self).__init__(**kwargs)

	def build(self):
		self.theme_cls.primary_palette = "DeepPurple"
		master = Builder.load_file("main.kv")
		return master

	def on_start(self):
            self.sock.connect((input("Enter the host : "), int(input("Enter the port : "))))
            self.sock.send(bytes(socket.gethostname(), "utf-8"))

	def receive(self):
		data = self.sock.recv(1024).decode("utf-8")
		return data

	def send(self, text):
		self.sock.send(bytes(text, "utf-8"))

	def _join_room(self, room_id):
		self.send(f"__join__|{room_id}")
		room_exists = eval(self.receive())
		if room_exists:
			self.root.current = "join_room"
			self.room_id = room_id
			self.root.ids.join_room.ids.nickname.text = socket.gethostname()
		else:
			print("room not exists")
			MDDialog(title="Room does not exist", text="You may create your own room.").open()

	def join_room(self, nick_name):
		self.send(f"__add__|{self.room_id}|{nick_name}")
		status = eval(self.receive())
		if not status:
			error_msg = self.receive()
			MDDialog(title="Error", text=error_msg).open()
			return 
		self.root.ids.chat_room.ids.toolbar.title = "Room " + self.room_id
		self.root.current = "chat_room"
		self.name = nick_name
		Clock.schedule_once(lambda x: Thread(target=self.chat, daemon=True).start(), 1)

	def chat(self):
		while True:
			message = self.sock.recv(1024).decode("utf-8")
			if not message : break
			print(message)
			if message.split("|")[0] == "__alert__":
				toast(message.split("|")[1] + " joined")
			else:
				message_bubble = MDFillRoundFlatButton(text=f"{message.split('|')[0].upper()}\n\n"+message.split('|')[1], size_hint=(None,None), md_bg_color = (74/255,67/255,156/255,1))
				root_card = MDAnchorLayout(size_hint=(1, None), anchor_x="left")
				primary_box = MDBoxLayout(orientation="vertical", size_hint=(None, None), width=self.root.width)
				primary_box.add_widget(root_card)
				root_card.add_widget(message_bubble)
				self.root.ids.chat_room.ids.chat_list.add_widget(primary_box)
			self.scroll_bottom()

	def send_message(self, message):
		self.send(f"__brodcast__|{self.room_id}|{self.name}|{message}")
		self.root.ids.chat_room.ids.message.text = ""
		message_bubble = MDFillRoundFlatButton(text="Me\n"+message, size_hint=(None,None), md_bg_color = (50/255,32/255,250/255,1))
		root_card = MDAnchorLayout(size_hint=(1, None), anchor_x="right")
		primary_box = MDBoxLayout(orientation="vertical", size_hint=(None, None), width=self.root.width)
		primary_box.add_widget(root_card)
		root_card.add_widget(message_bubble)
		self.root.ids.chat_room.ids.chat_list.add_widget(primary_box)
		self.scroll_bottom()

	def scroll_bottom(self):
		if self.root.ids.chat_room.ids.chat_view.scroll_y!=0:
			Animation.cancel_all(self.root.ids.chat_room.ids.chat_view, 'scroll_y')
			Animation(scroll_y=0, t='out_quad', d=.5).start(self.root.ids.chat_room.ids.chat_view)

ChatApp().run()
