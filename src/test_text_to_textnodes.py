import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_basic_text(self):
        text = "This is plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image(self):
        text = "This is an ![image](https://example.com/img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(result, expected)

    def test_link(self):
        text = "This is a [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_complex_example_from_assignment(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_mixed_formatting(self):
        text = "**Bold** and _italic_ and `code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_and_link_together(self):
        text = "![image](img.png) and [link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_nested_formatting_not_supported(self):
        # Note: Our implementation doesn't support nested formatting
        # This is expected behavior
        text = "**bold *italic* bold**"
        result = text_to_textnodes(text)
        # This will split bold first, leaving *italic* as plain text inside bold
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold *italic* bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_only_image(self):
        text = "![alt](url)"
        result = text_to_textnodes(text)
        expected = [TextNode("alt", TextType.IMAGE, "url")]
        self.assertEqual(result, expected)

    def test_only_link(self):
        text = "[text](url)"
        result = text_to_textnodes(text)
        expected = [TextNode("text", TextType.LINK, "url")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        text = "![first](1.png)![second](2.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("first", TextType.IMAGE, "1.png"),
            TextNode("second", TextType.IMAGE, "2.png"),
        ]
        self.assertEqual(result, expected)

    def test_processing_order(self):
        # Test that images are processed before links
        text = "![image](img.png)[link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
