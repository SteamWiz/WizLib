from . import DummyCommand


class ErrorCommand(DummyCommand):

    name = 'error'

    @DummyCommand.wrap
    def execute(self):
        return 2/0
