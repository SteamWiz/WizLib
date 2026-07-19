from test.dummy.command import DummyCommand
from wizlib.parser import WizParser


class SingCommand(DummyCommand):
    """Simple test of argument"""

    name = 'sing'

    @classmethod
    def add_args(self, parser: WizParser):
        parser.add_argument('song', default='yum', nargs='?')

    @DummyCommand.wrap
    def execute(self):
        return f"Singing {self.song}"
