import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_init_with_tag_and_children(self):
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])
        self.assertIsNone(parent.props)
        self.assertIsNone(parent.value)

    def test_init_with_tag_children_and_props(self):
        child = LeafNode("span", "text")
        props = {"class": "container", "id": "main"}
        parent = ParentNode("div", [child], props=props)
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, props)

    def test_to_html_with_single_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("p", "second")
        child3 = LeafNode("b", "third")
        parent = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent.to_html(),
            "<div><span>first</span><p>second</p><b>third</b></div>"
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], props={"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>text</span></div>')

    def test_to_html_with_multiple_props(self):
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        html = parent.to_html()
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertTrue(html.startswith("<div") and html.endswith("</div>"))

    def test_to_html_with_nested_parent_nodes(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_deeply_nested_parent_nodes(self):
        deepest = LeafNode("span", "deep")
        level4 = ParentNode("p", [deepest])
        level3 = ParentNode("article", [level4])
        level2 = ParentNode("section", [level3])
        level1 = ParentNode("div", [level2])
        expected = "<div><section><article><p><span>deep</span></p></article></section></div>"
        self.assertEqual(level1.to_html(), expected)

    def test_to_html_with_mixed_nested_and_sibling_nodes(self):
        nested_child = LeafNode("b", "bold")
        nested_parent = ParentNode("i", [nested_child])
        
        simple_leaf = LeafNode("p", "text")
        
        multi_child1 = LeafNode("em", "emphasized")
        multi_child2 = LeafNode("strong", "strong")
        multi_parent = ParentNode("span", [multi_child1, multi_child2])
        
        parent = ParentNode("div", [nested_parent, simple_leaf, multi_parent])
        expected = "<div><i><b>bold</b></i><p>text</p><span><em>emphasized</em><strong>strong</strong></span></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_nested_parents_and_props(self):
        child = LeafNode("span", "text")
        inner_parent = ParentNode("div", [child], props={"class": "inner"})
        outer_parent = ParentNode("section", [inner_parent], props={"id": "outer"})
        html = outer_parent.to_html()
        self.assertIn('id="outer"', html)
        self.assertIn('class="inner"', html)
        self.assertEqual(
            html,
            '<section id="outer"><div class="inner"><span>text</span></div></section>'
        )

    def test_to_html_without_tag_raises_error(self):
        child = LeafNode("span", "text")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertIn("tag", str(context.exception).lower())

    def test_to_html_with_no_children_raises_error(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertIn("children", str(context.exception).lower())

    def test_to_html_with_none_children_raises_error(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertIn("children", str(context.exception).lower())

    def test_to_html_with_all_leaf_node_types(self):
        children = [
            LeafNode("h1", "Heading"),
            LeafNode("p", "Paragraph"),
            LeafNode("a", "Link", props={"href": "http://example.com"}),
            LeafNode("img", "Image", props={"src": "image.png"}),
            LeafNode("code", "code"),
        ]
        parent = ParentNode("div", children)
        html = parent.to_html()
        self.assertIn("<h1>Heading</h1>", html)
        self.assertIn("<p>Paragraph</p>", html)
        self.assertIn('<a href="http://example.com">Link</a>', html)
        self.assertIn('<img src="image.png">Image</img>', html)
        self.assertIn("<code>code</code>", html)

    def test_to_html_with_complex_html_structure(self):
        title = LeafNode("h1", "Article Title")
        subtitle = LeafNode("p", "Subtitle", props={"class": "subtitle"})
        header = ParentNode("header", [title, subtitle])
        
        paragraph1 = LeafNode("p", "First paragraph.")
        paragraph2 = LeafNode("p", "Second paragraph.")
        content = ParentNode("article", [header, paragraph1, paragraph2])
        
        html = content.to_html()
        self.assertIn("<article>", html)
        self.assertIn("<header>", html)
        self.assertIn("<h1>Article Title</h1>", html)
        self.assertIn('<p class="subtitle">Subtitle</p>', html)
        self.assertIn("<p>First paragraph.</p>", html)
        self.assertIn("</article>", html)

    def test_to_html_with_multiple_levels_and_many_children(self):
        children1 = [LeafNode("li", f"Item {i}") for i in range(5)]
        ul = ParentNode("ul", children1)
        
        children2 = [LeafNode("td", f"Cell {i}") for i in range(3)]
        tr = ParentNode("tr", children2)
        
        body = ParentNode("div", [ul, tr])
        html = body.to_html()
        
        self.assertIn("<ul>", html)
        self.assertIn("<li>Item 0</li>", html)
        self.assertIn("<li>Item 4</li>", html)
        self.assertIn("<tr>", html)
        self.assertIn("<td>Cell 0</td>", html)
        self.assertIn("<td>Cell 2</td>", html)

    def test_to_html_special_characters_in_nested_structure(self):
        child = LeafNode("span", "<>&\"'")
        parent = ParentNode("div", [child])
        html = parent.to_html()
        self.assertIn("<>&\"'", html)
        self.assertEqual(html, "<div><span><>&\"'</span></div>")


if __name__ == "__main__":
    unittest.main()
