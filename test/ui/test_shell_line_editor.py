from io import StringIO
import os
from unittest.mock import Mock, patch

from wizlib.ui.shell.line_editor import ShellLineEditor
from wizlib.test_case import WizLibTestCase


class TestShellLineEditor(WizLibTestCase):

    def test_printable(self):
        e = ShellLineEditor()
        with \
                self.patch_ttyin('a\n'), \
                self.patcherr():
            r = e.edit()
        self.assertEqual(r, 'a')

    def test_tab(self):
        e = ShellLineEditor(['a-b', 'a-c'])
        with \
                self.patch_ttyin('a-\t\n'), \
                self.patcherr():
            r = e.edit()
        self.assertEqual(r, 'a-b')
