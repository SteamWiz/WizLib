from wizlib.test_case import WizLibTestCase

from test.dummy.command.sing_command import SingCommand
from wizlib.ui.shell_ui import ShellUI


class TestCommand(WizLibTestCase):

    def test_command(self):
        c = SingCommand(song='yo')
        r = c.execute()
        self.assertEqual(r, 'Singing yo')

    # def test_shell_ui(self):
    #     c = SingCommand(song='yo')
    #     self.assertIsInstance(c.ui, ShellUI)
