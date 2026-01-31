import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        markdown = "# Hello World"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_h1_with_whitespace(self):
        markdown = "   #   My Title   "
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")
    
    def test_no_h1_raises_exception(self):
        markdown = "## Not an h1\nSome text"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))
