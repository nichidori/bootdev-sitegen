import unittest

from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(textnodes, expected)

    def test_plain_text(self):
        text = "This is plain text"
        textnodes = text_to_textnodes(text)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(textnodes, expected)

    def test_only_bold(self):
        text = "This is **bold** text"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(textnodes, expected)

    def test_only_italic(self):
        text = "This is _italic_ text"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(textnodes, expected)

    def test_only_code(self):
        text = "This is `code` text"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(textnodes, expected)

    def test_only_image(self):
        text = "Here is ![image](url.jpg)"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.jpg"),
        ]
        self.assertEqual(textnodes, expected)

    def test_only_link(self):
        text = "Here is [link](url.html)"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.html"),
        ]
        self.assertEqual(textnodes, expected)

    def test_multiple_bold(self):
        text = "**bold1** and **bold2**"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
        ]
        self.assertEqual(textnodes, expected)

    def test_multiple_italic(self):
        text = "_italic1_ and _italic2_"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("italic1", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic2", TextType.ITALIC),
        ]
        self.assertEqual(textnodes, expected)

    def test_multiple_code(self):
        text = "`code1` and `code2`"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
        ]
        self.assertEqual(textnodes, expected)

    def test_bold_and_italic(self):
        text = "**bold** and _italic_"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(textnodes, expected)

    def test_code_and_image(self):
        text = "`code` and ![image](url.jpg)"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.jpg"),
        ]
        self.assertEqual(textnodes, expected)

    def test_empty_text(self):
        text = ""
        textnodes = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(textnodes, expected)

    def test_special_characters(self):
        text = "Text with !@#$%^&*()"
        textnodes = text_to_textnodes(text)
        expected = [TextNode("Text with !@#$%^&*()", TextType.TEXT)]
        self.assertEqual(textnodes, expected)

    def test_unmatched_delimiter(self):
        text = "Text with unmatched **bold"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_image_at_start(self):
        text = "![image](url.jpg) at start"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "url.jpg"),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(textnodes, expected)

    def test_link_at_end(self):
        text = "End with [link](url.html)"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.html"),
        ]
        self.assertEqual(textnodes, expected)
