from wizlib.test_case import WizLibTestCase

from template.command.do_command import DoCommand


class TestCommandDo(WizLibTestCase):

    def test_null(self):
        c = DoCommand()
        r = c.execute()
        self.assertEqual(r, 'Hello, World!')
