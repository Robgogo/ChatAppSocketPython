import tkinter as tk
from tkinter import scrolledtext
import socket
from threading import Thread
import _thread


class Server:
    def __init__(self, window):
        self.btn = tk.Button(window, text="Start Server",
                             command=self.handle_server)
        self.info_area = scrolledtext.ScrolledText(window, height=15)
        self.btn.place(x=200, y=0)
        self.info_area.place(x=0, y=50)
        self.btn.pack()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 13000
        self.server.bind((self.host, self.port))
        self.clients = []
        self.running = False

    def broadcast(self, msg, conn):
        for client in self.clients:
            if client != conn:
                try:
                    client.send(msg)
                except Exception as e:
                    print(e)
                    client.close()
                    self.remove(client)

    def client(self, conn, addr):
        conn.send("Welcome!".encode())
        while True:
            try:
                msg = conn.recv(2048)
                if msg:
                    if msg == b"quit\n":
                        conn.send("quit".encode())
                        conn.close()
                        self.remove(conn)
                        break
                    else:
                        msg_to_send = b"".join(
                            [b"<"+bytes(addr[0], encoding='utf8')+b">", msg])
                        self.broadcast(msg_to_send, conn)
                else:
                    self.remove(conn)
            except Exception as e:
                print(e)
                continue

    def remove(self, conn):
        if conn in self.clients:
            self.clients.remove(conn)

    def handle_server(self):
        if not self.running:
            self.btn.configure(text="Stop Server")
            self.info_area.insert(tk.INSERT, "Server running ...\n")
            self.info_area.insert(
                tk.INSERT, f"Running on {self.host}:{self.port}\n")
            self.running = not self.running
        else:
            self.btn.configure(text="Start Server")
            self.info_area.insert(tk.INSERT, "Server stoping ...\n")
            for conn in self.clients:
                conn.close()
            self.server.close()
            self.info_area.insert(tk.INSERT, "Server stoped\n")
            self.running = not self.running

    def accept(self):
        client_counter = 0
        while True:
            conn, addr = self.server.accept()
            self.clients.append(conn)
            self.info_area.insert(
                tk.INSERT, f"Client connected ,({addr[0]}:{addr[1]}\n")
            _thread.start_new_thread(self.client, (conn, addr))
            client_counter += 1


def on_closing():
    CONNECTION_THREAD.join()
    server_win.server.close()
    mainwindow.quit()


if __name__ == "__main__":

    mainwindow = tk.Tk()
    server_win = Server(mainwindow)
    server_win.server.listen(50)
    mainwindow.title("Server")
    mainwindow.geometry('400x400')
    CONNECTION_THREAD = Thread(target=server_win.accept)
    CONNECTION_THREAD.start()
    mainwindow.mainloop()
    CONNECTION_THREAD.join()
    server_win.server.close()
