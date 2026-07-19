
from test.dummy.command import DummyCommand
from wizlib.parser import WizParser


class DriveCommand(DummyCommand):
    """Simple test of config"""

    name = 'drive'
    speed: str = 'lazily'

    @classmethod
    def add_args(self, parser: WizParser):
        parser.add_argument('speed', default='fast', nargs='?')

    def execute(self):
        val = self.app.config.get('dummy-vehicle')
        if val:
            return f"Driving a {val} {self.speed}"
        else:
            return f"Stuck {self.speed}"
