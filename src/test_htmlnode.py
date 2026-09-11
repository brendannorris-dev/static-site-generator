import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()