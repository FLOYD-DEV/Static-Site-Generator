import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_present(self):
        markdown = "# My Awesome Title\n\nSome content here."
        self.assertEqual(extract_title(markdown), "My Awesome Title")

    def test_extract_title_whitespace(self):
        markdown = "#   Title with spaces   \n\nMore content."
        self.assertEqual(extract_title(markdown), "Title with spaces")

    def test_extract_title_no_h1(self):
        markdown = "## Secondary Title\n\nJust some text."
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_multiple_hashes(self):
        markdown = "### Not an h1\n# This is the one\nMore text."
        self.assertEqual(extract_title(markdown), "This is the one")

if __name__ == '__main__':
    unittest.main()