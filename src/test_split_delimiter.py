import unittest

from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual_new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        actual_new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_new_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_split_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        actual_new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_new_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_no_delimiters(self):
        node = TextNode("This is plain text", TextType.TEXT)
        actual_new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("This is plain text", TextType.TEXT),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_unmatched_delimiter(self):
        node = TextNode("This is text with `unmatched", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unmatched delimiter", str(context.exception))

    def test_multiple_pairs(self):
        node = TextNode("`code1` and `code2`", TextType.TEXT)
        actual_new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.TEXT)
        actual_new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_delimiter_at_end(self):
        node = TextNode("end with `code`", TextType.TEXT)
        actual_new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("end with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_non_text_node_passthrough(self):
        nodes = [
            TextNode("plain", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
        ]
        actual_new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("plain", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        actual_new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_multiple_nodes_with_mixed_types(self):
        nodes = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" `code` end", TextType.TEXT),
        ]
        actual_new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)


if __name__ == "__main__":
    unittest.main()
