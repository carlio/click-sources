from datetime import datetime

import click

from click_sources.exceptions import FileDoesNotExistException
from click_sources.impl.toml_source import TomlFileSource
from click_sources.options import Option, Options

from .base import ConfigSourceTestBase
from .utils import get_resource


class TestTomlFileSource(ConfigSourceTestBase):
    def test_null_path(self):
        self.assertRaises(ValueError, TomlFileSource, self._empty_options, None)

    def test_empty_file(self):
        source = TomlFileSource(self._empty_options, get_resource("emptyfile.txt"))
        self.assertEqual({}, source.get_parsed())

    def test_path_does_not_exist(self):
        self.assertRaises(
            FileDoesNotExistException, TomlFileSource, self._empty_options, get_resource("toml/does-not-exist.toml")
        )

    def test_valid_file(self):
        options = Options(
            [
                Option(["-e", "elephants"], type=bool),
                Option(["-n", "name"], type=str),
                Option(["-c", "count"], type=int),
                Option(["-b", "birthday"], type=click.DateTime()),
            ]
        )
        source = TomlFileSource(options, get_resource("toml/valid-config.toml"))
        self.assertEqual(
            {"elephants": True, "name": "barney", "count": 23, "birthday": datetime(year=1901, day=1, month=1)},
            source.get_parsed(),
        )
