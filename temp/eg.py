import tkinter as tk
from tkinter import filedialog
import socket
import os
BUFFER_SIZE = 4096

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill='both')
        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self)
        self.select_button["text"] = "Select a file"
        self.select_button["command"] = self.select_file
        self.select_button.pack(side="top", pady=10)

        self.send_button = tk.Button(self)
        self.send_button["text"] = "Send file"
        self.send_button["command"] = self.send_file
        self.send_button.pack(side="left", padx=10)

        self.receive_button = tk.Button(self)
        self.receive_button["text"] = "Receive file"
        self.receive_button["command"] = self.receive_file
        self.receive_button.pack(side="right", padx=10)

        # create a frame for the input boxes
        input_frame = tk.Frame(self)
        input_frame.pack(expand=True)

        # create an input box for the server IP address
        self.ip_label = tk.Label(input_frame, text="Server IP address:")
        self.ip_label.pack(side="left", padx=10, pady=10)
        self.ip_entry = tk.Entry(input_frame)
        self.ip_entry.pack(side="left", padx=10, pady=10)

        # create an input box for the server port number
        self.port_label = tk.Label(input_frame, text="Server port number:")
        self.port_label.pack(side="left", padx=10, pady=10)
        self.port_entry = tk.Entry(input_frame)
        self.port_entry.pack(side="left", padx=10, pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        print(f"Selected file: {self.file_path}")

    def send_file(self):
        # get the server IP address and port number from the user
        server_ip = self.ip_entry.get()
        server_port = int(self.port_entry.get())

        # create a socket and connect to the server
        s = socket.socket()
        s.connect((server_ip, server_port))

        # send the file metadata (name and size) to the server
        file_name = self.file_path.split("/")[-1]
        file_size = str(os.path.getsize(self.file_path))
        file_meta = f"{file_name},{file_size}"
        s.send(file_meta.encode())

        # send the file data to the server
        with open(self.file_path, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                s.sendall(data)

        # close the socket
        s.close()

    def receive_file(self):
        # get the server IP address and port number from the user
        server_ip = self.ip_entry.get()
        server_port = int(self.port_entry.get())

        # create a socket and connect to the server
        s = socket.socket()
        s.connect((server_ip, server_port))

        # receive file metadata
        file_meta = s.recv(BUFFER_SIZE).decode()
        file_name, file_size = file_meta.split(',')

        # convert file size to integer
        file_size = int(file_size)

        # receive the file data and save it to disk
        # receive the file data and save it to disk
        with open(file_name, 'wb') as f:
            remaining_bytes = int(file_size)
            while remaining_bytes > 0:
                    data = s.recv(BUFFER_SIZE)
                    f.write(data)
                    remaining_bytes -= len(data)

                    if remaining_bytes <= 0:
                        break
            print(os.path.abspath(file_name))
            # close the connection
            s.close()

        # close the socket
        s.close()

root = tk.Tk()
app = Application(master=root)
app.mainloop()