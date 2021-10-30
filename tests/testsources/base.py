from unittest import TestCase

from click_sources.options import Option, Options


class ConfigSourceTestBase(TestCase):

    _empty_options = Options([])
    _hello_options = Options([Option(["-h", "hello"], type=int, default=0)])
