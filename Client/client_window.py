import tkinter as tk
from tkinter import Entry, Label, scrolledtext
import socket
from threading import Thread
from tkinter.constants import DISABLED, NORMAL


class Client:
    def __init__(self, window):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.lbl1 = Label(window, text="host:")
        self.lbl2 = Label(window, text="port:")
        self.lbl3 = Label(window, text="Message:")
        self.t1 = Entry()
        self.t2 = Entry()
        self.t3 = Entry()
        self.btn = tk.Button(window, text="connect", command=self.connect)
        self.btn2 = tk.Button(window, text="Send", command=self.send)
        self.info_area = scrolledtext.ScrolledText(window)
        self.lbl1.place(x=0, y=10)
        self.t1.place(x=35, y=10)
        self.lbl2.place(x=210, y=10)
        self.t2.place(x=245, y=10)
        self.btn.place(x=450, y=10)
        self.lbl3.place(x=0, y=50)
        self.t3.place(x=65, y=50)
        self.btn2.place(x=250, y=50)
        self.info_area.place(x=0, y=90)
        # self.btn.pack()

    def connect(self):
        host = self.t1.get()
        port = int(self.t2.get())
        self.client.connect((host, port))
        RECIEVE_THREAD = Thread(target=self.recieve)
        RECIEVE_THREAD.start()
        self.btn['state'] = DISABLED

    def send(self):
        msg = self.t3.get()
        self.t3.delete(0, 'end')
        self.client.send(msg.encode())
        if msg == "quit":
            self.client.close()
            self.t1.delete(0, 'end')
            self.t2.delete(0, 'end')
            self.btn['state'] = NORMAL

    def recieve(self):
        while True:
            try:
                msg = self.client.recv(2048).decode()
                self.info_area.insert(tk.INSERT, msg+"\n")
            except Exception as e:
                print(e)
                break


def on_closing():
    client_win.client.send("quit".encode())
    mainwindow.quit()


mainwindow = tk.Tk()
client_win = Client(mainwindow)
mainwindow.title("Chat Client")
mainwindow.geometry('660x500')
mainwindow.protocol("WM_DELETE_WINDOW", on_closing)
mainwindow.mainloop()
