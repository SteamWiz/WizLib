
from wizlib.test_case import WizLibTestCase

from test.dummy import DummyApp
from wizlib.ui.shell_ui import ShellUI


class TestDefaultUI(WizLibTestCase):

    def test_command_ui(self):
        a = DummyApp()
        self.assertIsInstance(a.ui, ShellUI)
