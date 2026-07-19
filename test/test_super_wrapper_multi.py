from wizlib.test_case import WizLibTestCase
from unittest.mock import patch
from io import StringIO

from wizlib.super_wrapper import SuperWrapper


class TestSuperWrapperMulti(WizLibTestCase):

    def test_super_wrapper_multi(self):

        class Parent1(SuperWrapper):
            def execute(self, method, *args, **kwargs):
                print(f"Parent1 before")
                method(self, *args, **kwargs)
                print(f"Parent1 after")

        class Parent2(SuperWrapper):
            def execute(self, method, *args, **kwargs):
                print(f"Parent2 before")
                method(self, *args, **kwargs)
                print(f"Parent2 after")

        class Child(Parent1, Parent2):
            @Parent1.wrap
            @Parent2.wrap
            def execute(self, name):
                print(f"Hello {name}")

        with self.patchout() as o:
            c = Child()
            c.execute("Mary")
        o.seek(0)
        r = o.read()
        correct = """
            Parent1 before
            Parent2 before
            Hello Mary
            Parent2 after
            Parent1 after
        """.lstrip().split('\n')
        correct_clean = '\n'.join([i.lstrip() for i in correct])
        self.assertEqual(r, correct_clean)
