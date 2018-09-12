import os
import tempfile
import random
import string


class File:
    def __init__(self, path):
        self.path = path
        try:
            with open(os.path.join(tempfile.gettempdir(), self.path), 'r') as f:
                self.instance = f.read()
        except (FileNotFoundError, IOError) as e:
            # print('New File')
            self.instance = ''

    def write(self, text):
        with open(os.path.join(tempfile.gettempdir(), self.path), 'w') as f:
            self.instance = self.instance + text
            f.write(self.instance)

    def __add__(self, other):
        text = self.instance + other.instance
        path = random.choice(string.ascii_letters)
        new_file = File(path)
        new_file.write(text)
        return new_file

    def __getitem__(self, item):
        return self.instance.split('\n')[item]

    def __str__(self):
        return self.path

