
from argparse import ArgumentError
from wizlib.test_case import WizLibTestCase

from wizlib.parser import WizParser


def get_parser():
    example = WizParser()
    example.add_argument('--integer', type=int)
    example.add_argument('--choice', choices=['foo', 'bar'])
    sub_example = example.add_subparsers(dest='command')
    sub_sub_example = sub_example.add_parser('run')
    sub_sub_example.add_argument('--speed', choices=['fast', 'slow'])
    return example


class TestWizParser(WizLibTestCase):

    def test_valid1(self):
        example = get_parser()
        vals1 = example.parse_args(['--help'])
        self.assertIn('{foo,bar}', vals1.help)

    def test_valid2(self):
        example = get_parser()
        vals2 = example.parse_args(['run', '--help'])
        self.assertIn('{fast,slow}', vals2.help)

    def test_valid3(self):
        example = get_parser()
        vals = example.parse_args('--integer 12'.split())
        self.assertEqual(vals.integer, 12)

    # Test the speed fast option for accuracy
    def test_valid4(self):
        example = get_parser()
        vals = example.parse_args('run --speed fast'.split())
        self.assertEqual(vals.speed, 'fast')

    # Test the speed as 'stopped' and confirm the ArgumentError
    def test_invalid1(self):
        example = get_parser()
        with self.assertRaises(ArgumentError):
            example.parse_args('run --speed stopped'.split())

    # Test passing a string to the integer option and confirm the ArgumentError
    def test_invalid2(self):
        example = get_parser()
        with self.assertRaises(ArgumentError):
            example.parse_args('--integer s'.split())

    # Test an invalid option for the choice option and confirm the error
    def test_invalid3(self):
        example = get_parser()
        with self.assertRaises(ArgumentError):
            example.parse_args('--choice zee'.split())

    # Test an invalid command and confirm the error
    def test_invalid4(self):
        example = get_parser()
        with self.assertRaises(ArgumentError):
            example.parse_args('walk'.split())
