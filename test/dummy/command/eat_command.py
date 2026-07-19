
from test.dummy.command import DummyCommand
from wizlib.app import AppCancellation
from wizlib.command import CommandCancellation
from wizlib.ui import Choice, Chooser


class EatCommand(DummyCommand):

    name = 'eat'

    def handle_vals(self):
        super().handle_vals()
        if not self.provided('fruit'):
            chooser = Chooser('Pick one', None, [
                Choice('apples', 'a'),
                Choice('bananas', 'b'),
                Choice('cancel command', 'c'),
                Choice('Cancel app', 'C')
            ])
            choice = self.app.ui.get_option(chooser)
            if choice == 'cancel command':
                raise CommandCancellation('Sad')
            elif choice == 'Cancel app':
                raise AppCancellation('Disappointed')
            self.fruit = choice

    @DummyCommand.wrap
    def execute(self):
        return f"Yummy {self.fruit}"
