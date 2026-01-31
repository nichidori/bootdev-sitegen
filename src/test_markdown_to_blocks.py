import unittest

from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_paragraph(self):
        md = "This is a single paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_multiple_paragraphs(self):
        md = """First paragraph.

Second paragraph.

Third paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph.", "Second paragraph.", "Third paragraph."])

    def test_paragraphs_with_single_newlines(self):
        md = """This is paragraph one.
Still paragraph one.

This is paragraph two.
Still paragraph two."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is paragraph one.\nStill paragraph one.",
            "This is paragraph two.\nStill paragraph two."
        ])

    def test_leading_and_trailing_whitespace(self):
        md = """

First paragraph.


Second paragraph.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph.", "Second paragraph."])

    def test_only_whitespace(self):
        md = "   \n\n  \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_different_markdown_elements(self):
        md = """# Heading

Some paragraph text.

- List item 1
- List item 2

```
Code block
```

> Quote
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "# Heading",
            "Some paragraph text.",
            "- List item 1\n- List item 2",
            "```\nCode block\n```",
            "> Quote"
        ])

    def test_empty_blocks_between_content(self):
        md = """First block.



Second block."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block.", "Second block."])


if __name__ == "__main__":
    unittest.main()
