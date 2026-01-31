import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_simple_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_example_from_assignment(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_single_block(self):
        md = "Just a single block of text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single block of text"])

    def test_multiple_blank_lines(self):
        md = """First block


Second block after multiple newlines


Third block"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block after multiple newlines",
                "Third block",
            ],
        )

    def test_leading_trailing_whitespace(self):
        md = """   
   First block with spaces  
   
   Second block with tabs	
   
      Third block with indentation   
   """
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with spaces",
                "Second block with tabs",
                "Third block with indentation",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        md = "   \n\n\t\n   \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_blocks_with_newlines_inside(self):
        md = """Block 1 line 1
Block 1 line 2
Block 1 line 3

Block 2 line 1
Block 2 line 2

Block 3"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block 1 line 1\nBlock 1 line 2\nBlock 1 line 3",
                "Block 2 line 1\nBlock 2 line 2",
                "Block 3",
            ],
        )

    def test_list_blocks(self):
        md = """1. Ordered list item 1
2. Ordered list item 2
3. Ordered list item 3

- Unordered list item 1
- Unordered list item 2

* Another unordered list
* With asterisks"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "1. Ordered list item 1\n2. Ordered list item 2\n3. Ordered list item 3",
                "- Unordered list item 1\n- Unordered list item 2",
                "* Another unordered list\n* With asterisks",
            ],
        )

    def test_heading_blocks(self):
        md = """# Heading 1

## Heading 2

### Heading 3

Just a paragraph"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "## Heading 2",
                "### Heading 3",
                "Just a paragraph",
            ],
        )

    def test_quote_blocks(self):
        md = """> Quote line 1
> Quote line 2
> Quote line 3

Normal text

> Another quote"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "> Quote line 1\n> Quote line 2\n> Quote line 3",
                "Normal text",
                "> Another quote",
            ],
        )

    def test_mixed_content(self):
        md = """# Title

Introduction paragraph.

## Section 1

- Item 1
- Item 2
- Item 3

Some explanation here.

> Important note
> More details

Final thoughts."""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Title",
                "Introduction paragraph.",
                "## Section 1",
                "- Item 1\n- Item 2\n- Item 3",
                "Some explanation here.",
                "> Important note\n> More details",
                "Final thoughts.",
            ],
        )

    def test_windows_line_endings(self):
        md = "First block\r\n\r\nSecond block\r\n\r\nThird block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

    def test_mixed_line_endings(self):
        md = "First block\n\r\nSecond block\r\n\nThird block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("just a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("multiple\nlines\nparagraph"), BlockType.PARAGRAPH)
    
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Not headings
        self.assertEqual(block_to_block_type("####### Not heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#Not heading"), BlockType.PARAGRAPH)
    
    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\nprint('hello')\n```"), BlockType.CODE)
        
        # Not code blocks
        self.assertEqual(block_to_block_type("```\nincomplete"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("no backticks"), BlockType.PARAGRAPH)
    
    def test_quote(self):
        self.assertEqual(block_to_block_type("> quote line"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">quote line"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> line 1\n>line 2"), BlockType.QUOTE)
        
        # Not quotes
        self.assertEqual(block_to_block_type("> line 1\nnot quote"), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)
        
        # Not unordered lists
        self.assertEqual(block_to_block_type("-item 1"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- item 1\nnot list"), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2\n3. item 3"), BlockType.ORDERED_LIST)
        
        # Not ordered lists
        self.assertEqual(block_to_block_type("1.item 1"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. item 1\n3. item 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("0. item 1"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("2. item 1"), BlockType.PARAGRAPH)
    
    def test_edge_cases(self):
        # Empty block
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        
        # Single character
        self.assertEqual(block_to_block_type("a"), BlockType.PARAGRAPH)
        
        # Mixed content that looks like lists
        self.assertEqual(block_to_block_type("1. item\n- item"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
