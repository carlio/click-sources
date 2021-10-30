from datetime import datetime

import click

from click_sources.exceptions import FileDoesNotExistException, FileParseFailedException
from click_sources.impl.json_source import JsonFileSource
from click_sources.options import Option, Options

from .base import ConfigSourceTestBase
from .utils import get_resource


class TestJsonFileSource(ConfigSourceTestBase):
    def test_null_path(self):
        self.assertRaises(ValueError, JsonFileSource, self._empty_options, None)

    def test_empty_file(self):
        source = JsonFileSource(self._empty_options, get_resource("emptyfile.txt"))
        self.assertRaises(FileParseFailedException, source.get_parsed)

    def test_path_does_not_exist(self):
        self.assertRaises(
            FileDoesNotExistException, JsonFileSource, self._empty_options, get_resource("json/does-not-exist.json")
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
        source = JsonFileSource(options, get_resource("json/valid-config.json"))
        self.assertEqual(
            {"elephants": True, "name": "barney", "count": 23, "birthday": datetime(year=1901, day=1, month=1)},
            source.get_parsed(),
        )
