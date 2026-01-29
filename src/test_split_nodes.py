import unittest
from textnode import TextNode, TextType
from src.split_nodes import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        # Test when there's no delimiter in the text
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_single_bold_delimiter(self):
        # Test with single bold section
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_italic_delimiter(self):
        # Test with single italic section
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_code_delimiter(self):
        # Test with single code section
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_bold_sections(self):
        # Test with multiple bold sections
        node = TextNode("**Bold1** text **Bold2** more text **Bold3**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("Bold1", TextType.BOLD),
            TextNode(" text ", TextType.TEXT),
            TextNode("Bold2", TextType.BOLD),
            TextNode(" more text ", TextType.TEXT),
            TextNode("Bold3", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_beginning(self):
        # Test with delimiter at beginning
        node = TextNode("**Bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        # Test with delimiter at end
        node = TextNode("Text **Bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_only_delimited_text(self):
        # Test with only delimited text
        node = TextNode("**Bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter(self):
        # Test with unmatched delimiter (should raise exception)
        node = TextNode("**Bold** text **Bold", TextType.TEXT)
        
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertTrue("Unmatched delimiter" in str(context.exception))

    def test_empty_string(self):
        # Test with empty string
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_non_text_nodes_preserved(self):
        # Test that non-text nodes are preserved unchanged
        node1 = TextNode("**Bold** text", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("More **text**", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes(self):
        # Test with multiple input nodes
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("And this is *italic*", TextType.TEXT),
            TextNode("Plain text here", TextType.TEXT),
        ]
        
        # First split bold
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        # Then split italic on the result
        final_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("And this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("", TextType.TEXT),
            TextNode("Plain text here", TextType.TEXT),
        ]
        self.assertEqual(final_nodes, expected)

    def test_nested_delimiters(self):
        # Test that nested delimiters don't get confused
        node = TextNode("This is **bold** and this is *italic*", TextType.TEXT)
        
        # Split bold first
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Then split italic
        final_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(final_nodes, expected)

    def test_consecutive_delimiters(self):
        # Test with consecutive delimiters
        node = TextNode("**Bold****Still bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
            TextNode("Still bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
