import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
from io import StringIO
from argparse import ArgumentError

from test.dummy.command.math_command import MathCommand
from wizlib.app import RED
from wizlib.config_handler import ConfigHandler
from wizlib.error import ConfigHandlerError
from wizlib.test_case import WizLibTestCase
from wizlib.stream_handler import StreamHandler

from test.dummy import DummyApp
from test.dummy.command.dance_command import DanceCommand
from test.dummy.command.drive_command import DriveCommand
from test.dummy.command.eat_command import EatCommand
from test.dummy.command.own_command import OwnCommand


class DummyTest(WizLibTestCase):

    def test_input_stdin(self):
        with \
                self.patch_stream('laughter'), \
                self.patch_ttyin(), \
                self.patcherr() as o:
            DummyApp.start('dance')
            o.seek(0)
        self.assertIn('laughter', o.read())

    def test_loads(self):
        with self.patcherr(), self.patch_ttyin():
            DummyApp.start('dance')

    def test_default_command(self):
        with self.patchout() as o:
            DummyApp.start(debug=True)
        o.seek(0)
        self.assertIn('Stuck fast', o.read())

    def test_parse_run(self):
        with self.patchout() as o:
            DummyApp().parse_run('draw', '-c', 'straight')
        o.seek(0)
        self.assertIn('Curve was straight', o.read())

    def test_error_command(self):
        with self.assertRaises(ZeroDivisionError):
            DummyApp.start('error', debug=True)

    def test_cancel_command(self):
        with \
                self.patchout() as o, \
                self.patcherr(), \
                self.patch_ttyin("c"):
            a = DummyApp()
            c = EatCommand(a)
            c.execute()
        self.assertEqual('Sad', c.status)

    def test_not_debug(self):
        with self.patcherr() as e:
            try:
                DummyApp.start('error')
            except SystemExit:
                pass
        e.seek(0)
        self.assertIn(RED, e.read())

    def test_arg_provided(self):
        with self.patcherr() as o, self.patch_ttyin():
            DummyApp.start('dance', '--style', 'rumba')
        o.seek(0)
        self.assertIn('rumba', o.read())

    def test_wrong_arg(self):
        with self.assertRaises(ArgumentError):
            DummyApp.start('dance', '--wrestling', debug=True)

    def test_input_file(self):
        with self.patcherr() as o, \
                self.patch_ttyin():
            DummyApp.start('--stream', 'test/dummy/input.txt', 'dance')
        o.seek(0)
        self.assertIn('celebration', o.read())

    def test_config_default(self):
        with self.patchout() as o:
            DummyApp.start('--config', 'test/dummy/config.yml',
                           'drive', debug=True)
        o.seek(0)
        self.assertIn('Driving a motorcycle', o.read())

    def test_command_arg(self):
        with self.patchout() as o:
            DummyApp.start('sing', 'Crazy in Love', debug=True)
        o.seek(0)
        self.assertIn('Singing Crazy in Love', o.read())

    def test_fake_config(self):
        a = DummyApp()
        a.config = ConfigHandler.fake(dummy_vehicle='boat')
        c = DriveCommand(a)
        r = c.execute()
        self.assertIn('Driving a boat', r)

    def test_fake_multipart_config(self):
        a = DummyApp()
        a.config = ConfigHandler.fake(property_residence='house')
        c = OwnCommand(a)
        r = c.execute()
        self.assertIn('You own a house', r)

    def test_fake_input(self):
        a = DummyApp()
        with self.patch_stream('madly'), self.patch_ttyin(), \
                self.patcherr() as e:
            c = DanceCommand(a)
            r = c.execute()
        e.seek(0)
        self.assertIn('Dancing madly', e.read())

    def test_config_file_name(self):
        with TemporaryDirectory() as tempdir:
            with open(Path(tempdir) / '.dummy.yml', 'w') as file:
                file.write('dummy:\n  vehicle: airplane')
                file.seek(0)
            path = os.getcwd()
            try:
                os.chdir(tempdir)
                with self.patchout() as o:
                    DummyApp.start('drive', debug=True)
            finally:
                os.chdir(path)
            o.seek(0)
            self.assertIn('Driving a airplane', o.read())

    def test_null_on_no_config(self):
        with TemporaryDirectory() as tempdir:
            path = os.getcwd()
            try:
                os.chdir(tempdir)
                h = ConfigHandler()
                self.assertIsNone(h.get('f'))
            finally:
                os.chdir(path)

    def test_arg_name_collision(self):
        with self.patchout() as o:
            DummyApp.start('draw', '-c', 'wide')
        o.seek(0)
        self.assertIn('wide', o.read())

    # def test_config_default_command(self):
    #     with self.patchout() as o:
    #         DummyApp.start('--config', 'test/dummy/config.yml',
    #                        'drive', debug=True)
    #     o.seek(0)
    #     self.assertIn('Driving a motorcycle', o.read())

    def test_only_command(self):
        a = DummyApp()
        c = MathCommand(a, value=10.0)
        r = c.execute()
        self.assertEqual(6.0, r)

    def test_config_with_yaml_dict(self):
        """Test ConfigHandler with yaml dict parameter"""
        config_dict = {'dummy': {'vehicle': 'spaceship'}}
        h = ConfigHandler(data=config_dict)
        self.assertEqual('spaceship', h.get('dummy-vehicle'))

    def test_config_yaml_dict_with_env_precedence(self):
        """Test that environment variables take precedence over yaml dict"""
        config_dict = {'dummy': {'vehicle': 'spaceship'}}
        h = ConfigHandler(data=config_dict)
        with patch.dict(os.environ, {'DUMMY_VEHICLE': 'rocket'}):
            self.assertEqual('rocket', h.get('dummy-vehicle'))

    def test_config_yaml_dict_nested_keys(self):
        """Test nested keys in yaml dict"""
        config_dict = {'property': {'residence': 'castle'}}
        h = ConfigHandler(data=config_dict)
        self.assertEqual('castle', h.get('property-residence'))

    def test_config_yaml_dict_and_file_mutually_exclusive(self):
        """Test that yaml dict and file parameters work independently"""
        config_dict = {'dummy': {'vehicle': 'hovercraft'}}
        h1 = ConfigHandler(data=config_dict)
        h2 = ConfigHandler(file='test/dummy/config.yml')
        self.assertEqual('hovercraft', h1.get('dummy-vehicle'))
        self.assertEqual('motorcycle', h2.get('dummy-vehicle'))
