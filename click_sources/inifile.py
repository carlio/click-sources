import os
from configparser import ConfigParser, MissingSectionHeaderError

from .exceptions import FileDoesNotExistException, FileParseFailedException
from .options import Options


class IniFileSource:
    def __init__(self, options: Options, path: str, section: str):
        self._path = path
        self._options = options

        if path is None:
            raise ValueError("Path cannot be None")
        if not os.path.exists(path):
            raise FileDoesNotExistException(path)

        self._section = section

    def get_parsed(self):
        parser = ConfigParser()
        try:
            parser.read(self._path)
        except MissingSectionHeaderError:
            raise FileParseFailedException(f"The ini file {self._path} has no section header, and so is invalid")

        if not parser.has_section(self._section):
            return {}

        parsed = {}
        for option in self._options.iter_options():
            if parser.has_option(self._section, option.name):
                value = option.process_value({}, parser[self._section][option.name])
                parsed[option.name] = value

        return parsed
