from textnode import TextNode, TextType


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
