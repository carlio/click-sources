from click import Option as ClickOption


class Option(ClickOption):
    def __init__(self, *args, cli_only=False, **kwargs):
        self.cli_only = cli_only
        super().__init__(*args, **kwargs)


class Options:
    def __init__(self, options: [Option]):
        self._options = {o.name: o for o in options}

    def iter_options(self):
        return self._options.values()
