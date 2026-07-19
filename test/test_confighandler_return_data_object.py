
from test.dummy import DummyApp
from test.dummy.command.drive_command import DriveCommand
from wizlib.config_handler import ConfigHandler
from wizlib.test_case import WizLibTestCase


class TestConfigHandlerReturnDataObject(WizLibTestCase):

    def test_get_string(self):
        c = ConfigHandler(data={'a': 'b'})
        v = c.get('a')
        self.assertEqual('b', v)

    def test_get_dict(self):
        c = ConfigHandler(data={'a': {'b': 'c'}})
        v = c.get('a')
        self.assertEqual({'b': 'c'}, v)

    def test_get_list(self):
        c = ConfigHandler(data={'a': ['b', 'c']})
        v = c.get('a')
        self.assertEqual(['b', 'c'], v)

    def test_nested(self):
        c = ConfigHandler(data={'a': {'b': {'d': ['e', 'f']}}})
        v = c.get('a-b')
        self.assertEqual({'d': ['e', 'f']}, v)

    def test_inject_config_in_app_init(self):
        a = DummyApp(config={'dummy': {'vehicle': 'boat'}})
        c = DriveCommand(a)
        r = c.execute()
        self.assertIn('Driving a boat', r)
