from io import StringIO
import unittest
from wizlib.ui.text_wrapper import StreamingTextWrapper
from wizlib.test_case import WizLibTestCase


class TestStreamingTextWrapper(WizLibTestCase):

    def setUp(self):
        super().setUp()  # Call parent setUp to initialize notty patch
        self.output = StringIO()
        self.wrapper = StreamingTextWrapper(
            width=10, output_stream=self.output)

    def test_simple_text_no_wrapping(self):
        """Test writing simple text that doesn't need wrapping"""
        self.wrapper.write_streaming("hello")
        self.assertEqual(self.output.getvalue(), "hello")
        self.assertEqual(self.wrapper.current_column, 5)

    def test_word_wrapping_with_backspace(self):
        """Test word wrapping that triggers backspace correction"""
        # Write text that will cause wrapping: "hello world" (11 chars)
        # First "hello worl" will be written (10 chars, at limit)
        # Then 'd' will exceed, causing backspace of "world" and rewrap
        self.wrapper.write_streaming("hello world")

        # The output should contain backspaces and correction
        output = self.output.getvalue()
        self.assertIn('\b', output)  # Should contain backspace
        self.assertIn('\n', output)  # Should contain newline
        self.assertIn('world', output)  # Word should be present

    def test_explicit_newline_resets_column(self):
        """Test that explicit newlines reset column tracking"""
        self.wrapper.write_streaming("hello\nworld")
        # Should be at column 5 after "world"
        self.assertEqual(self.wrapper.current_column, 5)

    def test_multiple_spaces_handling(self):
        """Test handling of multiple spaces"""
        self.wrapper.write_streaming(
            # Two spaces (12 chars total - will wrap at width 10)
            "hello  world")
        output = self.output.getvalue()
        # The text should wrap because "hello  world" is 12 chars and width is
        # 10
        self.assertIn("hello", output)
        self.assertIn("world", output)
        self.assertIn('\n', output)  # Should contain newline from wrapping

    def test_long_word_no_break(self):
        """Test that words longer than width aren't broken"""
        self.wrapper.write_streaming("supercalifragilisticexpialidocious")
        output = self.output.getvalue()
        self.assertIn("supercalifragilisticexpialidocious", output)
        # Word should remain intact even if longer than width

    def test_color_code_handling(self):
        """Test writing text with color codes"""
        self.wrapper.write_streaming("hello", "\033[31m")  # Red color
        output = self.output.getvalue()
        self.assertIn("\033[31m", output)  # Should contain color code
        self.assertIn("\033[0m", output)   # Should contain reset code

    def test_write_newline_method(self):
        """Test explicit newline writing"""
        self.wrapper.write_streaming("hello")
        self.wrapper.write_newline()
        self.assertEqual(self.wrapper.current_column, 0)
        self.assertEqual(self.wrapper._word_buffer, [])

    def test_reset_position_method(self):
        """Test position reset functionality"""
        self.wrapper.write_streaming("hello")
        self.wrapper.reset_position()
        self.assertEqual(self.wrapper.current_column, 0)
        self.assertEqual(self.wrapper._word_buffer, [])

    def test_tab_character_handling(self):
        """Test handling of tab characters as word boundaries"""
        self.wrapper.write_streaming("hello\tworld")
        output = self.output.getvalue()
        self.assertIn("\t", output)

    def test_streaming_partial_words(self):
        """Test streaming characters of a word one by one"""
        # Simulate streaming behavior
        for char in "hello world":
            self.wrapper.write_streaming(char)

        output = self.output.getvalue()
        self.assertIn("hello", output)
        self.assertIn("world", output)

    def test_edge_case_empty_string(self):
        """Test handling of empty strings"""
        self.wrapper.write_streaming("")
        self.assertEqual(self.output.getvalue(), "")
        self.assertEqual(self.wrapper.current_column, 0)

    def test_width_boundary_exact_fit(self):
        """Test text that exactly fits the width"""
        # "1234567890" is exactly 10 characters
        self.wrapper.write_streaming("1234567890")
        self.assertEqual(self.wrapper.current_column, 10)

        # Adding one more character should wrap
        self.wrapper.write_streaming(" x")
        output = self.output.getvalue()
        self.assertIn("\n", output)
