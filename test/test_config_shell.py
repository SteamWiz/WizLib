import os
from subprocess import CompletedProcess
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import patch

from wizlib.error import ConfigHandlerError
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

    def test_config_yaml_shell_not_evaluated(self):
        with NamedTemporaryFile(mode='w+') as cfile:
            cfile.write('dummy:\n  vehicle: green $(echo Ducati)')
            cfile.seek(0)
            with self.patchout() as o:
                DummyApp.start('--config', cfile.name,
                               'drive', debug=True)
            o.seek(0)
            self.assertIn('Driving a green $(echo Ducati)', o.read())


class ConfigSecretTest(TestCase):

    @patch('wizlib.config_handler.subprocess.run')
    def test_op_reference_resolved(self, run):
        run.return_value = CompletedProcess(
            [], 0, stdout='s3cret\n', stderr='')
        c = ConfigHandler(data={'a': {'token': 'op://Private/ex/api-key'}})
        self.assertEqual('s3cret', c.get('a-token'))
        run.assert_called_once_with(
            ['op', 'read', 'op://Private/ex/api-key'],
            capture_output=True, text=True)
        self.assertNotIn('shell', run.call_args.kwargs)

    @patch('wizlib.config_handler.subprocess.run')
    def test_op_reference_stripped(self, run):
        run.return_value = CompletedProcess([], 0, stdout='x\n', stderr='')
        c = ConfigHandler(data={'t': '  op://V/My Item/f \n'})
        self.assertEqual('x', c.get('t'))
        self.assertEqual(['op', 'read', 'op://V/My Item/f'],
                         run.call_args.args[0])

    @patch('wizlib.config_handler.subprocess.run')
    def test_op_reference_cached(self, run):
        run.return_value = CompletedProcess([], 0, stdout='x\n', stderr='')
        c = ConfigHandler(data={'t': 'op://V/i/f'})
        c.get('t')
        c.get('t')
        run.assert_called_once()

    @patch('wizlib.config_handler.subprocess.run')
    def test_op_reference_failure(self, run):
        run.return_value = CompletedProcess(
            [], 1, stdout='', stderr='[ERROR] item not found\n')
        c = ConfigHandler(data={'t': 'op://V/i/f'})
        with self.assertRaises(ConfigHandlerError) as ctx:
            c.get('t')
        self.assertIn('item not found', str(ctx.exception))

    @patch('wizlib.config_handler.subprocess.run')
    def test_op_failure_names_key(self, run):
        run.return_value = CompletedProcess(
            [], 1, stdout='', stderr='[ERROR] not signed in\n')
        c = ConfigHandler(data={'myapp': {'token': 'op://V/i/f'}})
        with self.assertRaises(ConfigHandlerError) as ctx:
            c.get('myapp-token')
        message = str(ctx.exception)
        self.assertIn("'myapp-token'", message)
        self.assertIn('op://V/i/f', message)
        self.assertIn('not signed in', message)

    @patch('wizlib.config_handler.subprocess.run')
    def test_op_failure_names_explicit_path(self, run):
        run.return_value = CompletedProcess(
            [], 1, stdout='', stderr='[ERROR] not signed in\n')
        c = ConfigHandler(data={'myapp': {'api-token': 'op://V/i/f'}})
        with self.assertRaises(ConfigHandlerError) as ctx:
            c.get('myapp', 'api-token')
        self.assertIn("'myapp', 'api-token'", str(ctx.exception))

    @patch('wizlib.config_handler.subprocess.run')
    def test_op_missing(self, run):
        run.side_effect = FileNotFoundError('op')
        c = ConfigHandler(data={'t': 'op://V/i/f'})
        with self.assertRaises(ConfigHandlerError) as ctx:
            c.get('t')
        message = str(ctx.exception)
        self.assertIn('1Password CLI', message)
        self.assertIn('not found', message)
        self.assertIn("'t'", message)

    @patch('wizlib.config_handler.subprocess.run')
    def test_non_reference_string_stripped(self, run):
        c = ConfigHandler(data={'a': 'hello\n', 'b': '  padded  '})
        self.assertEqual('hello', c.get('a'))
        self.assertEqual('padded', c.get('b'))
        run.assert_not_called()

    def test_non_reference_yaml_block_stripped(self):
        with NamedTemporaryFile(mode='w+') as cfile:
            cfile.write('a: |\n  hello\n')
            cfile.seek(0)
            c = ConfigHandler(file=cfile.name)
            self.assertEqual('hello', c.get('a'))

    @patch('wizlib.config_handler.subprocess.run')
    def test_nested_reference_not_resolved(self, run):
        c = ConfigHandler(data={'s': {'token': 'op://V/i/f'}})
        self.assertEqual({'token': 'op://V/i/f'}, c.get('s'))
        run.assert_not_called()

    @patch('wizlib.config_handler.subprocess.run')
    def test_non_op_string_unchanged(self, run):
        c = ConfigHandler(data={'t': 'see op://V/i/f', 'u': '$(echo hi)',
                                'v': 'https://example.com/x'})
        self.assertEqual('see op://V/i/f', c.get('t'))
        self.assertEqual('$(echo hi)', c.get('u'))
        self.assertEqual('https://example.com/x', c.get('v'))
        run.assert_not_called()

    @patch.dict(os.environ, {'T': 'op://V/i/f'})
    @patch('wizlib.config_handler.subprocess.run')
    def test_env_not_resolved(self, run):
        c = ConfigHandler(data={'t': 'x'})
        self.assertEqual('op://V/i/f', c.get('t'))
        run.assert_not_called()
