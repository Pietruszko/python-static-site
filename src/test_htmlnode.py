import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        repr = HTMLNode()
        self.assertIsNotNone(repr)

    def test_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        node2 = HTMLNode("p", "1", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node2.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()
