import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b","Bold Text"),
                LeafNode(None, "Normal Text"),
                LeafNode("i", "Italic Text"),
                LeafNode(None, "Normal Text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold Text</b>Normal Text<i>Italic Text</i>Normal Text</p>"
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b","Bold Text"),
                LeafNode(None, "Normal Text"),
                LeafNode("i", "Italic Text"),
                LeafNode(None, "Normal Text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold Text</b>Normal Text<i>Italic Text</i>Normal Text</h2>"
        )

if __name__ == "__main__":
    unittest.main()