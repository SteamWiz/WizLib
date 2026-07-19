from wizlib.test_case import WizLibTestCase
from unittest.mock import patch
from io import StringIO

from wizlib.super_wrapper import SuperWrapper

correct = """
Parent execute before
IB execute before
    Hello Jane
    IB execute after
    Parent execute after
"""


class TestSuperWrapper(WizLibTestCase):

    def test_super_wrapper(self):

        class Parent(SuperWrapper):
            def execute(self, method, *args, **kwargs):
                print(f"Parent execute before")
                method(self, *args, **kwargs)
                print(f"Parent execute after")

        class InBetween(Parent):
            @Parent.wrap
            def execute(self, method, *args, **kwargs):
                print(f"IB execute before")
                method(self, *args, **kwargs)
                print(f"IB execute after")

        class NewChild(InBetween):
            @InBetween.wrap
            def execute(self, name):
                print(f"Hello {name}")

        with self.patchout() as o:
            c = NewChild()
            c.execute("Jane")
        o.seek(0)
        r = o.read()
        correct = """
            Parent execute before
            IB execute before
            Hello Jane
            IB execute after
            Parent execute after
        """.lstrip().split('\n')
        correct_clean = '\n'.join([i.lstrip() for i in correct])
        self.assertEqual(r, correct_clean)
