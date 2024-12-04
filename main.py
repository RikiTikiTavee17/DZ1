import os
import string
import tarfile
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess


class ShellEmulator:
    def __init__(self, username, hostname, fs_path, startup_script):
        self.username = username
        self.hostname = hostname
        self.file_path = os.path.join("", "C:\\Users\\Alexander\\PycharmProjects\\pythonProject3\\virtual_fs1")
        self.fs_path = fs_path
        self.startup_script = startup_script
        self.history = []

        # Распаковка файловой системы
        self.mount_filesystem()

        # GUI
        self.root = tk.Tk()
        self.root.title(f"{self.username}@{self.hostname} Shell Emulator")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill='x')
        self.entry.bind('<Return>', self.execute_command)

        self.load_startup_script()
        self.root.mainloop()

    def mount_filesystem(self):
        """Распаковать файловую систему из tar-файла."""
        with tarfile.open(self.fs_path) as tar:
            tar.extractall(path="virtual_fs")

    def load_startup_script(self):
        """Загрузить и выполнить стартовый скрипт."""
        if os.path.exists(self.startup_script):
            with open(self.startup_script) as f:
                for command in f:
                    self.execute_command(command.strip())

    def execute_command(self, event):
        command = self.entry.get()
        self.history.append(command)
        self.text_area.insert(tk.END, f"{self.username}@{self.hostname}: {command}\n")

        if command == "exit":
            self.root.quit()
        elif command == "clear":
            self.text_area.delete(1.0, tk.END)
        elif command == "history":
            self.show_history()
        elif command.startswith("cd"):
            self.change_directory(command[3:])
        elif command == "ls":
            self.list_directory()
        else:
            self.text_area.insert(tk.END, f"Command not found: {command}\n")

        self.entry.delete(0, tk.END)

    def show_history(self):
        history_str = "\n".join(self.history)
        self.text_area.insert(tk.END, history_str)

    def change_directory(self, path):
        try:
            os.chdir(os.path.join(self.file_path, path))
            self.file_path = os.path.join(self.file_path, path)
            self.text_area.insert(tk.END, f"Changed directory to {path}\n")
        except FileNotFoundError:
            self.text_area.insert(tk.END, f"No such directory: {path}\n")

    def list_directory(self):
        try:
            files = os.listdir(self.file_path)
            self.text_area.insert(tk.END, "\n".join(files) + "\n")
        except Exception as e:
            self.text_area.insert(tk.END, str(e) + "\n")


if __name__ == "__main__":
    ShellEmulator("User", "localhost", "virtual_fs.tar", "script.sh")
