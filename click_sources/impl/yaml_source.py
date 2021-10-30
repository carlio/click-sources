import typing as t

import yaml

from ..source import FileConfigSource


class YamlFileSource(FileConfigSource):
    def get_parsed(self) -> t.Dict[str, t.Any]:
        with open(self._path) as f:
            content = yaml.load(f, Loader=yaml.SafeLoader)
            if not content:
                return {}
            # cast back into string so that click can take care of type parsing...
            # TODO: something better than this...
            return self._type_cast_dict({k: str(v) for k, v in content.items()})
