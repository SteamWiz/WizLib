from argparse import ArgumentParser

from . import DummyCommand


class MathCommand(DummyCommand):

    name = 'math'

    @classmethod
    def add_args(self, parser: ArgumentParser):
        parser.add_argument('--value', type=float)

    @DummyCommand.wrap
    def execute(self):
        return self.value * 0.6
