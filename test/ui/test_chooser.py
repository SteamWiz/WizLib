from wizlib.test_case import WizLibTestCase

from wizlib.ui import Choice, Chooser


class TestChooser(WizLibTestCase):

    def test_by_key(self):
        chooser = Chooser(intro="go?", default="ok")
        chooser.add_choice('ok', 'yY\n', True)
        chooser.add_choice('cancel', 'c', False)
        choice = chooser.choice_by_key('c')
        self.assertEqual(choice, False)

    def test_by_2nd_key(self):
        chooser = Chooser(intro="go?", default="ok")
        chooser.add_choice('ok', 'yY\n')
        chooser.add_choice('cancel', 'c')
        choice = chooser.choice_by_key('Y')
        self.assertEqual(choice, 'ok')

    def test_return_key(self):
        chooser = Chooser(intro="go?", default="ok")
        chooser.add_choice('ok', 'yY\n')
        chooser.add_choice('cancel', 'c')
        choice = chooser.choice_by_key('\n')
        self.assertEqual(choice, 'ok')

    def test_prompt_not_in_text(self):
        choice = Choice('doit', 'xyz')
        self.assertEqual(choice.key_prompt, '(x)doit')

    def test_init_chooser_short(self):
        c = Chooser('Pick one', 'pizza', choices={
                    'h': 'hamburger', 'do': 'hot dog', 'p': 'pizza'})
        self.assertEqual(
            c.prompt_string, 'Pick one [pizza] (h)amburger hot (d)og: ')

    def test_hit_test(self):
        c = Choice('abc')
        self.assertTrue(c.hit_text('ab'))

    def test_choose_by_text(self):
        c = Chooser(None, None, [Choice('abc'), Choice('xyz'), Choice('abd')])
        self.assertEqual(len(c.choices_by_text('ab')), 2)

    def test_short_form_text_options(self):
        c = Chooser(None, None, ['abc', 'xyz', 'abd'])
        self.assertEqual(len(c.choices_by_text('ab')), 2)

    # def test_by_word(self):
    #     chooser = Chooser(intro="w?")
    #     chooser.add_choice(keys=['a'], text='ab', action='g')
    #     chooser.add_choice(keys=['x'], text='xy', action='h')
    #     choice = chooser.choice_by_word('xy')
    #     self.assertEqual(choice, 'h')
