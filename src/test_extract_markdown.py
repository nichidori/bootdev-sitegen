import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev)")
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_extract_multiple_images(self):
        text = "![img1](url1) and ![img2](url2)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("img1", "url1"), ("img2", "url2")], matches)

    def test_extract_multiple_links(self):
        text = "[link1](url1) and [link2](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link1", "url1"), ("link2", "url2")], matches)

    def test_extract_mixed_images_and_links(self):
        text = "![image](img.jpg) and [link](page.html)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([("image", "img.jpg")], images)
        self.assertListEqual([("link", "page.html")], links)

    def test_extract_no_images(self):
        matches = extract_markdown_images("This is plain text with no images")
        self.assertListEqual([], matches)

    def test_extract_no_links(self):
        matches = extract_markdown_links("This is plain text with no links")
        self.assertListEqual([], matches)

    def test_extract_empty_alt_text_image(self):
        matches = extract_markdown_images("![](/path/to/img.png)")
        self.assertListEqual([("", "/path/to/img.png")], matches)

    def test_extract_empty_link_text(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_image_with_spaces(self):
        matches = extract_markdown_images("![my image](https://example.com/img.png)")
        self.assertListEqual([("my image", "https://example.com/img.png")], matches)

    def test_extract_link_with_spaces(self):
        matches = extract_markdown_links("[click here](https://example.com)")
        self.assertListEqual([("click here", "https://example.com")], matches)

    def test_extract_image_with_special_chars(self):
        matches = extract_markdown_images("![img!@#](url?query=value)")
        self.assertListEqual([("img!@#", "url?query=value")], matches)

    def test_extract_link_with_special_chars(self):
        matches = extract_markdown_links("[link!@#](url?query=value)")
        self.assertListEqual([("link!@#", "url?query=value")], matches)

    def test_extract_images_in_text(self):
        text = "Start ![img1](url1) middle ![img2](url2) end"
        matches = extract_markdown_images(text)
        self.assertListEqual([("img1", "url1"), ("img2", "url2")], matches)

    def test_extract_links_in_text(self):
        text = "Start [link1](url1) middle [link2](url2) end"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link1", "url1"), ("link2", "url2")], matches)

    def test_extract_empty_string(self):
        self.assertListEqual([], extract_markdown_images(""))
        self.assertListEqual([], extract_markdown_links(""))


if __name__ == "__main__":
    unittest.main()
