import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_basic(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_spaces(self):
        markdown = "#   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_not_first_line(self):
        markdown = "Some text\n# Title Here"
        self.assertEqual(extract_title(markdown), "Title Here")

    def test_extract_title_multiple_headings(self):
        markdown = "# First Title\n## Second Heading\n# Another Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_extract_title_no_title(self):
        markdown = "No title here\nJust some text"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")

    def test_extract_title_empty_string(self):
        markdown = ""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")

    def test_extract_title_only_whitespace(self):
        markdown = "   \n\t\n"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")

    def test_extract_title_wrong_heading_level(self):
        markdown = "## Not a title\n# This is the title"
        self.assertEqual(extract_title(markdown), "This is the title")

    def test_extract_title_with_newlines(self):
        markdown = "# Title\n\nSome content"
        self.assertEqual(extract_title(markdown), "Title")


if __name__ == "__main__":
    unittest.main()
