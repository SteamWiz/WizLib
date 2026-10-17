import os
from subprocess import CompletedProcess
from unittest import TestCase
from unittest.mock import patch

from wizlib.config_handler import ConfigHandler


DATA = {
    'filez4eva': {
        'classify': {
            'auto-threshold': 7,
            'label': 'plain',
        },
        'tool-use': {'limit': 3},
    }
}


class TestConfigHandlerExplicitPath(TestCase):

    def test_hyphenated_key_reachable(self):
        c = ConfigHandler(data=DATA)
        self.assertEqual(
            7, c.get('filez4eva', 'classify', 'auto-threshold'))

    def test_hyphenated_key_not_reachable_single_arg(self):
        c = ConfigHandler(data=DATA)
        self.assertIsNone(c.get('filez4eva-classify-auto-threshold'))

    def test_hyphenated_intermediate_key(self):
        c = ConfigHandler(data=DATA)
        self.assertEqual(3, c.get('filez4eva', 'tool-use', 'limit'))

    def test_explicit_path_returns_dict(self):
        c = ConfigHandler(data=DATA)
        self.assertEqual({'limit': 3}, c.get('filez4eva', 'tool-use'))

    @patch.dict(os.environ, {'FILEZ4EVA_CLASSIFY_AUTO_THRESHOLD': '9'})
    def test_env_override(self):
        c = ConfigHandler(data=DATA)
        self.assertEqual(
            '9', c.get('filez4eva', 'classify', 'auto-threshold'))

    @patch.dict(os.environ, {'FILEZ4EVA_CLASSIFY_AUTO_THRESHOLD': ''})
    def test_empty_env_ignored(self):
        c = ConfigHandler(data=DATA)
        self.assertEqual(
            7, c.get('filez4eva', 'classify', 'auto-threshold'))

    def test_caching_on_tuple(self):
        data = {'a': {'b-c': 'first'}}
        c = ConfigHandler(data=data)
        self.assertEqual('first', c.get('a', 'b-c'))
        data['a']['b-c'] = 'second'
        self.assertEqual('first', c.get('a', 'b-c'))
        self.assertIn(('a', 'b-c'), c.cache)

    def test_single_and_tuple_no_collision(self):
        c = ConfigHandler(
            data={'a': {'b': {'c': 'nested'}, 'b-c': 'literal'}})
        self.assertEqual('nested', c.get('a-b-c'))
        self.assertEqual('literal', c.get('a', 'b-c'))
        self.assertEqual('nested', c.get('a-b-c'))

    def test_single_arg_unchanged(self):
        c = ConfigHandler(data={'a': {'b': 'c'}})
        self.assertEqual('c', c.get('a-b'))
        self.assertIn('a-b', c.cache)

    @patch.dict(os.environ, {'A_B': 'env'})
    def test_single_arg_env_unchanged(self):
        c = ConfigHandler(data={'a': {'b': 'c'}})
        self.assertEqual('env', c.get('a-b'))

    def test_fake_single_arg(self):
        c = ConfigHandler.fake(filez4eva_host='x')
        self.assertEqual('x', c.get('filez4eva-host'))

    def test_fake_explicit_path(self):
        c = ConfigHandler.fake(filez4eva_classify_auto_threshold=5)
        self.assertEqual(
            5, c.get('filez4eva', 'classify', 'auto-threshold'))
        self.assertNotIn(('filez4eva', 'classify', 'auto-threshold'), c.cache)

    def test_shell_syntax_not_evaluated(self):
        c = ConfigHandler(data={'a': {'b-c': '$(echo hello)'}})
        self.assertEqual('$(echo hello)', c.get('a', 'b-c'))

    @patch('wizlib.config_handler.subprocess.run')
    def test_op_reference_resolved(self, run):
        run.return_value = CompletedProcess([], 0, stdout='hello\n',
                                            stderr='')
        c = ConfigHandler(data={'a': {'b-c': 'op://V/i/f'}})
        self.assertEqual('hello', c.get('a', 'b-c'))
        run.assert_called_once_with(['op', 'read', 'op://V/i/f'],
                                    capture_output=True, text=True)

    def test_missing_returns_none_uncached(self):
        c = ConfigHandler(data=DATA)
        self.assertIsNone(c.get('filez4eva', 'classify', 'nope'))
        self.assertNotIn(('filez4eva', 'classify', 'nope'), c.cache)

    def test_path_through_non_dict(self):
        c = ConfigHandler(data=DATA)
        self.assertIsNone(c.get('filez4eva', 'classify', 'label', 'x'))

    def test_no_args_raises(self):
        c = ConfigHandler(data=DATA)
        with self.assertRaises(TypeError):
            c.get()
