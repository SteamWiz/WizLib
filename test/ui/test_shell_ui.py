from io import StringIO
import os
import sys
from wizlib.test_case import WizLibTestCase
from unittest.mock import patch
from test.dummy import DummyApp

from wizlib.ui import UI
from wizlib.ui.shell import ESC
from wizlib.ui.shell_ui import ShellUI


class TestShellUI(WizLibTestCase):

    def test_exists(self):
        u = UI.family_member('name', 'shell')()
        self.assertIsInstance(u, ShellUI)

    def test_output(self):
        u = UI.family_member('name', 'shell')()
        with self.patcherr() as e:
            u.send('j')
        e.seek(0)
        self.assertEqual(e.read(), ESC + '[36mj' + ESC + '[0m\n')

    def test_word_wrapping_disabled_by_default(self):
        """Test that wrapping is disabled by default (wrap=0)"""
        u = UI.family_member('name', 'shell')()
        with self.patcherr() as e:
            u.send('this is a very long line that would ' +
                   'normally wrap but should not')
        e.seek(0)
        output = e.read()
        # Should not contain backspaces or unwanted newlines from wrapping
        self.assertNotIn('\b', output)
        self.assertIn('this is a very long line', output)

    def test_word_wrapping_enabled(self):
        """Test that wrapping works when explicitly enabled"""
        u = UI.family_member('name', 'shell')()
        with self.patcherr() as e:
            # Use wrap=20 to force wrapping on longer text
            u.send('this is a long line that ' +
                   'should wrap at some point', wrap=20)
        e.seek(0)
        output = e.read()
        # Should contain a newline from wrapping
        lines = output.split('\n')
        self.assertGreater(len(lines), 1)

    def test_streaming_text_with_wrapper(self):
        """Test multiple streaming calls with wrapper maintain state"""
        u = UI.family_member('name', 'shell')()
        with self.patcherr() as e:
            # Send parts of a sentence that would wrap
            u.send('this is a ', newline=False, wrap=15)
            u.send('longer sentence that ', newline=False, wrap=15)
            u.send('wraps', wrap=15)
        e.seek(0)
        output = e.read()
        # Should contain wrapping behavior (check for individual characters and
        # backspaces) Check for individual chars since they have color codes
        self.assertIn('t', output)
        self.assertIn('w', output)
        # Should have backspaces from wrapping correction
        self.assertIn('\b', output)
        self.assertIn('\n', output)  # Should have newlines from wrapping

    def test_wrapper_instance_reuse(self):
        """Test that wrapper instance is reused for same width"""
        with self.patcherr():
            u = UI.family_member('name', 'shell')()

            # First call should create wrapper
            u.send('test1', wrap=20)
            first_wrapper = u._wrapper

            # Second call with same width should reuse wrapper
            u.send('test2', wrap=20)
            self.assertIs(u._wrapper, first_wrapper)

            # Different width should create new wrapper
            u.send('test3', wrap=30)
            self.assertIsNot(u._wrapper, first_wrapper)
            self.assertEqual(u._wrapper.width, 30)

    def test_get_option(self):
        with \
                self.patchout() as o, \
                self.patcherr(), \
                self.patch_ttyin('a'):
            DummyApp.start('eat')
        o.seek(0)
        self.assertEqual('Yummy apples', o.read())

    def test_get_text_from_user(self):
        with \
                self.patchout() as o, \
                self.patcherr(), \
                self.patch_ttyin("I love cheese\n"):
            DummyApp.start('talk')
        o.seek(0)
        self.assertEqual('You said "I love cheese"', o.read())

    def test_default_option_key(self):
        with \
                self.patchout() as o, \
                self.patch_ttyin("\n"):
            DummyApp.start('thank')
        o.seek(0)
        self.assertEqual('You said yes', o.read())
