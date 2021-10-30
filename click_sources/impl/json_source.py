import json
import typing as t
from json import JSONDecodeError

from ..exceptions import FileParseFailedException
from ..source import FileConfigSource


class JsonFileSource(FileConfigSource):
    def get_parsed(self) -> t.Dict[str, t.Any]:
        with open(self._path) as f:
            try:
                return self._type_cast_dict(json.load(f))
            except JSONDecodeError as e:
                raise FileParseFailedException from e
