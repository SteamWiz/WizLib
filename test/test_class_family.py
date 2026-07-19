from test.data_class_family.atriarch import Atriarch
from wizlib.test_case import WizLibTestCase


class TestClassFamily(WizLibTestCase):

    def test_family_children(self):
        cx = Atriarch.family_children()
        self.assertEqual(len(cx), 1)
