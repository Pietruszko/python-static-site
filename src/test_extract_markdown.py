import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    # Tests for extract_markdown_images
    def test_extract_images_no_images(self):
        text = "This is just plain text with no images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_images_single_image(self):
        text = "Here's an image: ![alt text](https://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(result, expected)

    def test_extract_images_multiple_images(self):
        text = "![first](https://example.com/1.png) and ![second](https://example.com/2.png)"
        result = extract_markdown_images(text)
        expected = [
            ("first", "https://example.com/1.png"),
            ("second", "https://example.com/2.png")
        ]
        self.assertEqual(result, expected)

    def test_extract_images_with_text_around(self):
        text = "Text before ![alt](img.png) text after"
        result = extract_markdown_images(text)
        expected = [("alt", "img.png")]
        self.assertEqual(result, expected)

    def test_extract_images_empty_alt_text(self):
        text = "![](image.jpg)"
        result = extract_markdown_images(text)
        expected = [("", "image.jpg")]
        self.assertEqual(result, expected)

    def test_extract_images_complex_url(self):
        text = "![complex](https://example.com/path/to/image.jpg?width=100&height=200)"
        result = extract_markdown_images(text)
        expected = [("complex", "https://example.com/path/to/image.jpg?width=100&height=200")]
        self.assertEqual(result, expected)

    def test_extract_images_nested_brackets(self):
        text = "![alt [with] brackets](image.png)"
        result = extract_markdown_images(text)
        # Should not match because alt text contains brackets
        self.assertEqual(result, [])

    def test_extract_images_parentheses_in_url(self):
        text = "![alt](https://example.com/image(1).png)"
        result = extract_markdown_images(text)
        # Should not match because URL contains parentheses
        self.assertEqual(result, [])

    # Tests for extract_markdown_links
    def test_extract_links_no_links(self):
        text = "This is just plain text with no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_links_single_link(self):
        text = "Here's a link: [link text](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("link text", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_links_multiple_links(self):
        text = "[first](https://example.com/1) and [second](https://example.com/2)"
        result = extract_markdown_links(text)
        expected = [
            ("first", "https://example.com/1"),
            ("second", "https://example.com/2")
        ]
        self.assertEqual(result, expected)

    def test_extract_links_with_text_around(self):
        text = "Text before [link](https://example.com) text after"
        result = extract_markdown_links(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_links_empty_link_text(self):
        text = "[](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_links_complex_url(self):
        text = "[complex](https://example.com/path/to/page?query=string&another=param)"
        result = extract_markdown_links(text)
        expected = [("complex", "https://example.com/path/to/page?query=string&another=param")]
        self.assertEqual(result, expected)

    def test_extract_links_not_images(self):
        text = "![image](img.png) and [link](https://example.com)"
        result = extract_markdown_links(text)
        # Should only extract the link, not the image
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_links_mixed_images_and_links(self):
        text = "![img1](1.png) [link1](1.com) ![img2](2.png) [link2](2.com)"
        result = extract_markdown_links(text)
        expected = [
            ("link1", "1.com"),
            ("link2", "2.com")
        ]
        self.assertEqual(result, expected)

    # Tests to ensure images and links don't get confused
    def test_extract_images_does_not_extract_links(self):
        text = "[not an image](https://example.com)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_links_does_not_extract_images(self):
        text = "![not a link](image.png)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_both_separately(self):
        text = "Image: ![alt](img.png) Link: [text](url.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertEqual(images, [("alt", "img.png")])
        self.assertEqual(links, [("text", "url.com")])

    def test_extract_links_adjacent_to_images(self):
        text = "![image](img.png)[link](url.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertEqual(images, [("image", "img.png")])
        self.assertEqual(links, [("link", "url.com")])

    def test_extract_links_with_nested_brackets(self):
        text = "[link [with] brackets](url.com)"
        result = extract_markdown_links(text)
        # Should not match because link text contains brackets
        self.assertEqual(result, [])

    def test_extract_links_parentheses_in_url(self):
        text = "[link](https://example.com/page(1).html)"
        result = extract_markdown_links(text)
        # Should not match because URL contains parentheses
        self.assertEqual(result, [])

    # Edge cases
    def test_empty_string(self):
        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_links(""), [])

    def test_only_whitespace(self):
        self.assertEqual(extract_markdown_images("   \n\t  "), [])
        self.assertEqual(extract_markdown_links("   \n\t  "), [])

    def test_malformed_markdown(self):
        text = "![missing closing bracket] (url.com)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_malformed_markdown_links(self):
        text = "[missing closing bracket] (url.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_partial_matches(self):
        text = "![partial"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extra_spaces(self):
        text = "![  alt  ](  url.com  )"
        result = extract_markdown_images(text)
        # Note: spaces are included in the capture
        expected = [("  alt  ", "  url.com  ")]
        self.assertEqual(result, expected)

    def test_multiline_text(self):
        text = """First line with ![image](img.png)
        Second line with [link](url.com)
        Third line with another ![image2](img2.png)"""
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertEqual(images, [("image", "img.png"), ("image2", "img2.png")])
        self.assertEqual(links, [("link", "url.com")])


if __name__ == "__main__":
    unittest.main()
