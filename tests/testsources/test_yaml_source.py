from datetime import datetime
from unittest import TestCase

import click

from click_sources.exceptions import FileDoesNotExistException
from click_sources.impl.yaml_source import YamlFileSource
from click_sources.options import Option, Options

from .utils import get_resource

_empty_options = Options([])
_hello_options = Options([Option(["-h", "hello"], type=int, default=0)])


class TestYamlFileSource(TestCase):
    def test_null_path(self):
        self.assertRaises(ValueError, YamlFileSource, _empty_options, None)

    def test_empty_file(self):
        source = YamlFileSource(_empty_options, get_resource("emptyfile.txt"))
        self.assertEqual(source.get_parsed(), {})

    def test_path_does_not_exist(self):
        self.assertRaises(
            FileDoesNotExistException, YamlFileSource, _empty_options, get_resource("yaml/does-not-exist.yaml")
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
        source = YamlFileSource(options, get_resource("yaml/valid-config.yaml"))
        self.assertEqual(
            {"elephants": True, "name": "barney", "count": 23, "birthday": datetime(year=1901, day=1, month=1)},
            source.get_parsed(),
        )
