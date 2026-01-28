import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init_with_all_arguments(self):
        node = LeafNode("p", "Hello", props={"class": "text"})
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.props, {"class": "text"})
        self.assertIsNone(node.children)

    def test_init_minimal_arguments(self):
        node = LeafNode("span", "Text content")
        self.assertEqual(node.value, "Text content")
        self.assertEqual(node.tag, "span")
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_to_html_with_tag_and_value(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_tag_value_and_props(self):
        node = LeafNode("a", "Click here", props={"href": "http://example.com"})
        self.assertEqual(node.to_html(), '<a href="http://example.com">Click here</a>')

    def test_to_html_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_without_value_raises_error(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_string_value_raises_error(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_props_to_html_inherited(self):
        node = LeafNode("div", "Content", props={"id": "main", "class": "container"})
        props_html = node.props_to_html()
        self.assertIn('id="main"', props_html)
        self.assertIn('class="container"', props_html)

    def test_props_to_html_no_props(self):
        node = LeafNode("div", "Content")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = LeafNode("p", "Hello", props={"id": "greeting"})
        self.assertEqual(repr(node), "LeafNode(p, Hello, {'id': 'greeting'})")

    def test_repr_no_props(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(repr(node), "LeafNode(p, Hello, None)")


if __name__ == "__main__":
    unittest.main()
