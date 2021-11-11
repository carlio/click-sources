import abc
import os
import typing as t

from .exceptions import FileDoesNotExistException
from .options import Options


class ConfigSource(abc.ABC):
    def __init__(self, options: Options):
        self._options = options

    @abc.abstractmethod
    def get_parsed(self) -> t.Dict[str, t.Any]:
        raise NotImplementedError

    def _type_cast_dict(self, data: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        parsed = {}
        for option in self._options.iter_options():
            value = data.get(option.name)
            if value is not None:
                value = option.process_value({}, value)
                parsed[option.name] = value
        return parsed


class FileConfigSource(ConfigSource, abc.ABC):
    def __init__(self, options: Options, path: str):
        super().__init__(options)
        self._path = path

        if path is None:
            raise ValueError("Path cannot be None")
        if not os.path.exists(path):
            raise FileDoesNotExistException(path)
