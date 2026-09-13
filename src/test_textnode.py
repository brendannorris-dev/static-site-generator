import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_converter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from blocktype import block_to_block_type, BlockType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("This is not a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value,"This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value,"This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value,"This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value,"This is a link node")
        self.assertEqual(html_node.props, {"href":"https://example.com/cat.png"})

    def test_img(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value,"")
        self.assertEqual(html_node.props, {"src":"https://example.com/cat.png", "alt": "This is an image node"})

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                        [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT)
                        ] )

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
                    [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("bold", TextType.BOLD),
                        TextNode(" word", TextType.TEXT)
                    ] )
        
    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,
                    [
                        TextNode("This is text with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word", TextType.TEXT)
                    ] )

    def test_nontext_node(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        text = TextNode("has `code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([bold_node, text], "`", TextType.CODE)
        self.assertEqual(len(new_nodes),4)
        self.assertEqual(new_nodes,
                         [
                             TextNode("already bold", TextType.BOLD),
                             TextNode("has ", TextType.TEXT),
                             TextNode("code", TextType.CODE),
                             TextNode(" here", TextType.TEXT)
                         ])

    def test_multiple_sections(self):
        node = TextNode("Bold **words** are **great**, right?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                             TextNode("Bold ", TextType.TEXT),
                             TextNode("words", TextType.BOLD),
                             TextNode(" are ", TextType.TEXT),
                             TextNode("great", TextType.BOLD),
                             TextNode(", right?", TextType.TEXT)
                         ])

    def test_delimiter_at_start(self):
        node = TextNode("**Bold** words are great", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes),2)
        self.assertEqual(new_nodes,
                         [
                             TextNode("Bold", TextType.BOLD),
                             TextNode(" words are great", TextType.TEXT)
                         ])
        
    def test_delimiter_at_end(self):
        node = TextNode("Bold words are **great**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes),2)
        self.assertEqual(new_nodes,
                          [
                              TextNode("Bold words are ", TextType.TEXT),
                              TextNode("great", TextType.BOLD)
                          ])

    def test_whole_delimited(self):
        node = TextNode("**Bold is amazing**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes),1)
        self.assertEqual(new_nodes,
                         [
                             TextNode("Bold is amazing", TextType.BOLD)
                         ])

    def test_unclosed_delimiter(self):
        node = TextNode("Oopsies, forgot to **end bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_no_delimiter(self):
        node = TextNode("Oops, no markdown!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                             TextNode("Oops, no markdown!", TextType.TEXT)])

    def test_empty_list(self):
        new_nodes = split_nodes_delimiter([], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_multiple_text_nodes(self):
        node1 = TextNode("This is **bold** node1", TextType.TEXT)
        node2 = TextNode("This is **bold** node2", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1,node2], '**', TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is ", TextType.TEXT),
                             TextNode("bold", TextType.BOLD),
                             TextNode(" node1", TextType.TEXT),
                             TextNode("This is ", TextType.TEXT),
                             TextNode("bold", TextType.BOLD),
                             TextNode(" node2", TextType.TEXT)
                         ])

    def test_all_nontext_nodes(self):
        node1 = TextNode("This is bold1", TextType.BOLD)
        node2 = TextNode("This is code1", TextType.CODE)
        new_nodes = split_nodes_delimiter([node1, node2], '**', TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is bold1", TextType.BOLD),
                             TextNode("This is code1", TextType.CODE)
                         ])

    def test_image_markdown_test(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches,
                         [
                             ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                             ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
                         ])

    def test_link_markdown_test(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches,
                         [
                             ("to boot dev", "https://www.boot.dev"),
                             ("to youtube", "https://www.youtube.com/@bootdotdev")
                         ])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )

    def test_split_image_single(self):
        node = TextNode("![image](https://www.example.COM/IMAGE.PNG)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG")],
            new_nodes
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode("This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT)
            ],
            new_nodes
        )

    def test_full_totextnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_node
        )

    def test_markdown_to_blocks(self):
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

    def test_heading_block(self):
        block = "### This is a header"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_code_block(self):
        block = """```
This is code
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote_block(self):
        block = """> This is
> a quote"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unorder_block(self):
        block = """- Item 1
- Item 2"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_order_block(self):
        block = """1. Item 1
2. Item 2"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is a normal paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_broken_header_block(self):
        block = "####### Broken Header"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_broken_ordered_block(self):
        block = """1. Item 1
3. Item 3"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_broken_quote_block(self):
        block = """> This is
not a quote"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

        
if __name__ == "__main__":
    unittest.main()