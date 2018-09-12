class FileReader:
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        try:
            with open(self.path, 'r') as f:
                return f.read()
        except IOError:
            return ""
