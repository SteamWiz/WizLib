from tempfile import NamedTemporaryFile
from wizlib.test_case import WizLibTestCase
from wizlib.config_handler import ConfigHandler

from test.dummy import DummyApp
from test.dummy.command.drive_command import DriveCommand


class ConfigShellTest(WizLibTestCase):

    def test_config_yaml(self):
        with NamedTemporaryFile(mode='w+') as cfile:
            cfile.write('dummy:\n  vehicle: nothing\n')
            cfile.seek(0)
            with self.patchout() as o:
                DummyApp.start('--config', cfile.name,
                               'drive', debug=True)
            o.seek(0)
            self.assertIn('Driving a nothing', o.read())

    def test_config_yaml_shell(self):
        with NamedTemporaryFile(mode='w+') as cfile:
            cfile.write('dummy:\n  vehicle: green $(echo Ducati)')
            cfile.seek(0)
            with self.patchout() as o:
                DummyApp.start('--config', cfile.name,
                               'drive', debug=True)
            o.seek(0)
            self.assertIn('Driving a green Ducati', o.read())
