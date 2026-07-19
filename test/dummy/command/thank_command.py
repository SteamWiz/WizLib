
from test.dummy.command import DummyCommand
from wizlib.ui import Choice, Chooser


class ThankCommand(DummyCommand):

    name = 'thank'

    def handle_vals(self):
        super().handle_vals()
        if not self.provided('fruit'):
            chooser = Chooser('Feeling grateful?', 'yes', [
                Choice('yes', 'Yy'),
                Choice('no', 'Nn')
            ])
            self.choice = self.app.ui.get_option(chooser)

    @DummyCommand.wrap
    def execute(self):
        return f"You said {self.choice}"
