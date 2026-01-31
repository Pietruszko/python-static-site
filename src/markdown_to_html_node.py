from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks
from text_to_textnodes import text_to_textnodes
from text_node_to_html_node import text_node_to_html_node


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        if node.text.strip():  
            html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def heading_block_to_html_node(block):
    level = 0
    for i in range(len(block)):
        if block[i] == "#":
            level += 1
        else:
            break
    
    if level > 6:
        level = 6
    
    content = block[level:].strip()
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)
    

def paragraph_block_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(line.strip() for line in lines)
    children = text_to_children(text)
    return ParentNode("p", children)


def code_block_to_html_node(block):
    lines = block.split("\n")
    
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        code_lines = lines[1:-1]
        code_content = "\n".join(code_lines)
        if code_lines:  # Add trailing newline if there's content
            code_content += "\n"
        code_node = LeafNode("code", code_content)
        return ParentNode("pre", [code_node])
    # ... rest


def quote_block_to_html_node(block):
    lines = block.split("\n")
    quote_lines = []
    
    for line in lines:
        if line.startswith(">"):
            line = line[1:].lstrip()
        quote_lines.append(line)
    
    quote_text = " ".join(quote_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        if line.startswith("- "):
            item_text = line[2:].strip()
            children = text_to_children(item_text)
            item_node = ParentNode("li", children)
            list_items.append(item_node)
    
    return ParentNode("ul", list_items)


def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    
    for i, line in enumerate(lines):
        parts = line.split(". ", 1)
        if len(parts) == 2 and parts[0].isdigit():
            item_text = parts[1].strip()
            children = text_to_children(item_text)
            item_node = ParentNode("li", children)
            list_items.append(item_node)
    
    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    """Convert a full markdown document to an HTML node."""
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            node = heading_block_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_block_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_block_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_block_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_block_to_html_node(block)
        else:  # PARAGRAPH
            node = paragraph_block_to_html_node(block)
        
        html_nodes.append(node)
    
    return ParentNode("div", html_nodes)
