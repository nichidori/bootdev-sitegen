import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div", value="Content", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple(self):
        node = HTMLNode(tag="img", value=None, props={"src": "image.png", "alt": "An image"})
        self.assertEqual(node.props_to_html(), ' src="image.png" alt="An image"')

    def test_all_arguments(self):
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", value="Parent", children=[child1, child2], props={"class": "container"})
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.value, "Parent")
        self.assertEqual(parent.children, [child1, child2])
        self.assertEqual(parent.props, {"class": "container"})


if __name__ == "__main__":
    unittest.main()
