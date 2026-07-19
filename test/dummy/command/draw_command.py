from test.dummy.command import DummyCommand
from wizlib.parser import WizParser


class DrawCommand(DummyCommand):
    """If a command arg overlaps with a base arg"""

    name = 'draw'

    @classmethod
    def add_args(self, parser: WizParser):
        parser.add_argument('--curve', '-c')

    @DummyCommand.wrap
    def execute(self):
        return f"Curve was {self.curve}"
