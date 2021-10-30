class FileDoesNotExistException(Exception):
    def __init__(self, path):
        self.path = path
        super().__init__(f"Config file {path} does not exist")


class FileParseFailedException(Exception):
    pass
