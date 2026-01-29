from src.textnode import TextNode, TextType
from src.extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        elif delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
        else:
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Unmatched delimiter")
            for i, node in enumerate(parts):
                t_type = TextType.TEXT if i % 2 == 0 else text_type
                new_nodes.append(TextNode(node, t_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        
        if not images:
            new_nodes.append(old_node)
            continue
        
        remaining_text = text
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            
            index = remaining_text.find(image_markdown)
            if index == -1:
                continue
            
            if index > 0:
                new_nodes.append(TextNode(remaining_text[:index], TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            remaining_text = remaining_text[index + len(image_markdown):]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        
        if not links:
            new_nodes.append(old_node)
            continue
        
        remaining_text = text
        for link_text, url in links:
            link_markdown = f"[{link_text}]({url})"
            
            index = remaining_text.find(link_markdown)
            if index == -1:
                continue
            
            if index > 0:
                new_nodes.append(TextNode(remaining_text[:index], TextType.TEXT))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            
            remaining_text = remaining_text[index + len(link_markdown):]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes
