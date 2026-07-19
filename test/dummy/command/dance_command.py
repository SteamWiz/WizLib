from argparse import ArgumentParser

from wizlib.ui import Choice, Chooser

from . import DummyCommand


class DanceCommand(DummyCommand):
    """Simple test of stream handler"""

    name = 'dance'

    @classmethod
    def add_args(self, parser: ArgumentParser):
        parser.add_argument('--style')

    def handle_vals(self):
        super().handle_vals()
        if not self.provided('style'):
            self.style = self.app.stream.text

    @DummyCommand.wrap
    def execute(self):
        self.app.ui.send(f"Dancing {self.style}")
        new = self.app.ui.get_text('Next dance? ')
        if new:
            self.app.ui.send(f'Dancing {new}')
