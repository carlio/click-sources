from datetime import datetime

import click

from click_sources.exceptions import FileDoesNotExistException, FileParseFailedException
from click_sources.impl.ini_source import IniFileSource
from click_sources.options import Option, Options

from .base import ConfigSourceTestBase
from .utils import get_resource


class TestIniFileSource(ConfigSourceTestBase):
    def test_null_path(self):
        self.assertRaises(ValueError, IniFileSource, self._empty_options, None, "parse_me")

    def test_empty_file(self):
        source = IniFileSource(self._empty_options, get_resource("emptyfile.txt"), "parse_me")
        self.assertEqual(source.get_parsed(), {})

    def test_path_does_not_exist(self):
        self.assertRaises(
            FileDoesNotExistException,
            IniFileSource,
            self._empty_options,
            get_resource("ini/does-not-exist.ini"),
            "parse_me",
        )

    def test_no_section(self):
        source = IniFileSource(self._hello_options, get_resource("ini/no-section.ini"), "parse_me")
        self.assertRaises(FileParseFailedException, source.get_parsed)

    def test_section_missing(self):
        source = IniFileSource(self._hello_options, get_resource("ini/without-section.ini"), "parse_me")
        self.assertEqual(source.get_parsed(), {})

    def test_section_present(self):
        source = IniFileSource(self._hello_options, get_resource("ini/with-section.ini"), "parse_me")
        self.assertEqual(source.get_parsed(), {"hello": 1})

    def test_bad_types(self):
        options = Options(
            [
                Option(["-h", "hello"], type=int, default=0),
                Option(["-e", "eat_fish"], type=bool),
                Option(["-o", "oink"], type=str),
            ]
        )
        source = IniFileSource(options, get_resource("ini/bad-types.ini"), "parse_me")
        self.assertRaises(click.BadParameter, source.get_parsed)

    def test_valid_file(self):
        options = Options(
            [
                Option(["-e", "elephants"], type=bool),
                Option(["-n", "name"], type=str),
                Option(["-c", "count"], type=int),
                Option(["-b", "birthday"], type=click.DateTime()),
            ]
        )
        source = IniFileSource(options, get_resource("ini/valid-config.ini"), "parse_this")
        self.assertEqual(
            {"elephants": True, "name": "barney", "count": 23, "birthday": datetime(year=1901, day=1, month=1)},
            source.get_parsed(),
        )
