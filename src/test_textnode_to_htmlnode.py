import unittest

from textnode import TextNode, TextType
from textnode_to_htmlnode import text_node_to_html_node
from leafnode import LeafNode


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_conversion(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props)

    def test_text_with_special_characters(self):
        node = TextNode("Hello <world> & 'friends'", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello <world> & 'friends'")

    def test_text_empty_string(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertIsNone(html_node.tag)

    def test_text_with_numbers(self):
        node = TextNode("12345 67.89", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "12345 67.89")

    def test_bold_text_conversion(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")
        self.assertIsNone(html_node.props)

    def test_bold_text_single_word(self):
        node = TextNode("Bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold")

    def test_bold_text_with_spaces(self):
        node = TextNode("   bold with spaces   ", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "   bold with spaces   ")

    def test_italic_text_conversion(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")
        self.assertIsNone(html_node.props)

    def test_italic_text_single_word(self):
        node = TextNode("Emphasis", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Emphasis")

    def test_code_text_conversion(self):
        node = TextNode("const x = 5;", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "const x = 5;")
        self.assertIsNone(html_node.props)

    def test_code_text_with_special_chars(self):
        node = TextNode("if (x > 5) { return true; }", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "if (x > 5) { return true; }")

    def test_code_text_with_html_tags(self):
        node = TextNode("<div class='test'>HTML</div>", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "<div class='test'>HTML</div>")

    def test_link_conversion(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_link_with_different_urls(self):
        urls = [
            "https://example.com",
            "http://example.com",
            "/relative/path",
            "example.com",
            "https://example.com/path?query=value#anchor",
        ]
        for url in urls:
            with self.subTest(url=url):
                node = TextNode("link", TextType.LINK, url=url)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, "a")
                self.assertEqual(html_node.props["href"], url)

    def test_link_with_empty_text(self):
        node = TextNode("", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_link_with_special_url_characters(self):
        node = TextNode(
            "Search",
            TextType.LINK,
            url="https://example.com/search?q=hello%20world&lang=en",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(
            html_node.props["href"],
            "https://example.com/search?q=hello%20world&lang=en",
        )

    def test_image_conversion(self):
        node = TextNode("alt text", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": node.text})

    def test_image_with_relative_path(self):
        node = TextNode("logo", TextType.IMAGE, url="/images/logo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "/images/logo.png")

    def test_image_with_empty_alt_text(self):
        node = TextNode("", TextType.IMAGE, url="/path/to/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "/path/to/image.jpg")

    def test_image_with_data_url(self):
        data_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
        node = TextNode("embedded", TextType.IMAGE, url=data_url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], data_url)

    def test_returns_leafnode_instance(self):
        node = TextNode("text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)

    def test_all_types_return_leafnode(self):
        test_cases = [
            (TextType.TEXT, "text", None),
            (TextType.BOLD, "bold", None),
            (TextType.ITALIC, "italic", None),
            (TextType.CODE, "code", None),
            (TextType.LINK, "link", "https://example.com"),
            (TextType.IMAGE, "image", "/path/image.png"),
        ]
        for text_type, text, url in test_cases:
            with self.subTest(text_type=text_type):
                if url:
                    node = TextNode(text, text_type, url=url)
                else:
                    node = TextNode(text, text_type)
                html_node = text_node_to_html_node(node)
                self.assertIsInstance(html_node, LeafNode)

    def test_long_text_content(self):
        long_text = "a" * 1000
        node = TextNode(long_text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, long_text)

    def test_text_with_newlines(self):
        text_with_newlines = "Line 1\nLine 2\nLine 3"
        node = TextNode(text_with_newlines, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, text_with_newlines)

    def test_text_with_tabs(self):
        text_with_tabs = "Column1\tColumn2\tColumn3"
        node = TextNode(text_with_tabs, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, text_with_tabs)

    def test_bold_text_html_rendering(self):
        node = TextNode("Important", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Important</b>")

    def test_italic_text_html_rendering(self):
        node = TextNode("Emphasized", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Emphasized</i>")

    def test_code_text_html_rendering(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>print('hello')</code>")

    def test_link_html_rendering(self):
        node = TextNode("Google", TextType.LINK, url="https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://google.com">Google</a>')

    def test_image_html_rendering(self):
        node = TextNode("test image", TextType.IMAGE, url="test.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="test.png" alt="test image"></img>')

    def test_invalid_text_type_raises_exception(self):
        class InvalidTextType:
            pass

        node = TextNode("text", InvalidTextType())
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertIn("Unsupported TextType", str(context.exception))

    def test_unicode_text_conversion(self):
        unicode_text = "Hello 世界 🌍"
        node = TextNode(unicode_text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, unicode_text)

    def test_unicode_in_all_types(self):
        unicode_text = "café"
        test_cases = [
            TextType.BOLD,
            TextType.ITALIC,
            TextType.CODE,
        ]
        for text_type in test_cases:
            with self.subTest(text_type=text_type):
                node = TextNode(unicode_text, text_type)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.value, unicode_text)


if __name__ == "__main__":
    unittest.main()
