
from test.dummy.command import DummyCommand


class TalkCommand(DummyCommand):

    name = 'talk'

    def handle_vals(self):
        super().handle_vals()
        if not self.provided('topic'):
            self.topic = self.app.ui.get_text(
                'What? ', ['something', 'nothing', 'jo-first', 'jo-second'],
                'everything')

    @DummyCommand.wrap
    def execute(self):
        return f'You said "{self.topic}"'
