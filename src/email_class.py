class Email:
    def __init__(self,file_name, path, subject, text):
        self.file_name = file_name
        self.path = path
        self.subject = subject
        self.text = text

    def __eq__(self, other):
        if self.file_name == other.file_name and self.path == other.path and self.subject == other.subject and self.text == other.text:
            return True
        else:
            return False
