import typing as t

import toml

from ..source import FileConfigSource


class TomlFileSource(FileConfigSource):
    def get_parsed(self) -> t.Dict[str, t.Any]:
        with open(self._path) as f:
            content = toml.load(f)
            # cast back into string so that click can take care of type parsing...
            # TODO: something better than this...
            return self._type_cast_dict({k: str(v) for k, v in content.items()})
