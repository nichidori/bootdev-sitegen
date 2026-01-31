import unittest

from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
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
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
        ]
        self.assertEqual(actual_new_nodes, expected_new_nodes)

    def test_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.TEXT)
        actual_new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_new_nodes = [
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


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode("Here is an ![image](url.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.jpg"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_images(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_image_at_start(self):
        node = TextNode("![image](url.jpg) at start", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "url.jpg"),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_image_at_end(self):
        node = TextNode("End with ![image](url.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.jpg"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_images_no_text_after(self):
        node = TextNode("![img1](url1)![img2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node_passthrough(self):
        nodes = [
            TextNode("text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_image_with_spaces_in_alt(self):
        node = TextNode("![my image](url.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("my image", TextType.IMAGE, "url.jpg"),
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode("Here is a [link](url.html)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.html"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_links(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_link_at_start(self):
        node = TextNode("[link](url.html) at start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "url.html"),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_link_at_end(self):
        node = TextNode("End with [link](url.html)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.html"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_links_no_text_after(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node_passthrough(self):
        nodes = [
            TextNode("text", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_link_with_spaces_in_text(self):
        node = TextNode("[click here](url.html)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("click here", TextType.LINK, "url.html"),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
