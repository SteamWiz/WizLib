
from test.dummy.command import DummyCommand


class OwnCommand(DummyCommand):
    """est of multipart config key"""

    name = 'own'

    def execute(self):
        val = self.app.config.get('property-residence')
        if val:
            return f"You own a {val}"
        else:
            return "Stuck"
