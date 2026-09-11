import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(
            "This is an HTMLNode", 
            "This is the value of the HTMLNode", 
            None, 
            {
                "href": "https://www.google.com",
                "target": "_blank",
            })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_eq(self):
        node = HTMLNode("NodeA", "ValueA", None, None)
        node2 = HTMLNode("NodeA", "ValueA", None, None)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode("NodeA", "ValueA", None, None)
        node2 = HTMLNode("NodeB", "ValueB", None, None)
        self.assertNotEqual(node, node2)

    def test_values(self):
        node = HTMLNode("NodeA", "ValueA", None, None)
        self.assertEqual(node.tag, "NodeA")
        self.assertEqual(node.value, "ValueA")

    def test_repr(self):
        node = HTMLNode("NodeA", "ValueA", None, None)
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(NodeA, ValueA, children: None, None)"
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_node(self):
        node = LeafNode("b", "wow", None)
        node2 = LeafNode("b", "wow", None)
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)

    def test_leaf_node_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_node_no_tag(self):
        node = LeafNode(None, "wowza", None)
        self.assertEqual(node.to_html(), "wowza")

if __name__ == "__main__":
    unittest.main()