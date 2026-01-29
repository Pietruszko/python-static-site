from textnode import TextNode
from textnode import TextType

def main():
    text_node = TextNode("abc", TextType.BOLD, "www.abc.com")
    print(text_node)

main()
