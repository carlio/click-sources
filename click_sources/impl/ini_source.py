import typing as t
from configparser import ConfigParser, MissingSectionHeaderError

from ..exceptions import FileParseFailedException
from ..options import Options
from ..source import FileConfigSource


class IniFileSource(FileConfigSource):
    def __init__(self, options: Options, path: str, section: str):
        super().__init__(options, path)
        self._section = section

    def get_parsed(self) -> t.Dict[str, t.Any]:
        parser = ConfigParser()
        try:
            parser.read(self._path)
        except MissingSectionHeaderError:
            raise FileParseFailedException(f"The ini file {self._path} has no section header, and so is invalid")

        if not parser.has_section(self._section):
            return {}

        return self._type_cast_dict(parser[self._section])
