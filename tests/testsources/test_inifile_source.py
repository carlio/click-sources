from unittest import TestCase

from click import BadParameter

from click_sources.exceptions import FileDoesNotExistException, FileParseFailedException
from click_sources.inifile import IniFileSource
from click_sources.options import Option, Options

from .utils import get_resource

_empty_options = Options([])
_hello_options = Options([Option(["-h", "hello"], type=int, default=0)])


class TestIniFileSource(TestCase):
    def test_null_path(self):
        self.assertRaises(ValueError, IniFileSource, _empty_options, None, "parse_me")

    def test_empty_file(self):
        source = IniFileSource(_empty_options, get_resource("empty.ini"), "parse_me")
        self.assertEqual(source.get_parsed(), {})

    def test_path_does_not_exist(self):
        self.assertRaises(
            FileDoesNotExistException, IniFileSource, _empty_options, get_resource("does-not-exist.ini"), "parse_me"
        )

    def test_no_section(self):
        source = IniFileSource(_hello_options, get_resource("no-section.ini"), "parse_me")
        self.assertRaises(FileParseFailedException, source.get_parsed)

    def test_section_missing(self):
        source = IniFileSource(_hello_options, get_resource("without-section.ini"), "parse_me")
        self.assertEqual(source.get_parsed(), {})

    def test_section_present(self):
        source = IniFileSource(_hello_options, get_resource("with-section.ini"), "parse_me")
        self.assertEqual(source.get_parsed(), {"hello": 1})

    def test_bad_types(self):
        options = Options(
            [
                Option(["-h", "hello"], type=int, default=0),
                Option(["-e", "eat_fish"], type=bool),
                Option(["-o", "oink"], type=str),
            ]
        )
        source = IniFileSource(options, get_resource("bad-types.ini"), "parse_me")
        self.assertRaises(BadParameter, source.get_parsed)
