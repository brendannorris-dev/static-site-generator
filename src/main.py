from textnode import TextNode, TextType

from markdown_html import markdown_to_html_node

def main():
    #test = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    #print(test.__repr__())

    test = """## This is a header

- Item 1
- Item 2

Regular text"""

    print(markdown_to_html_node(test))

main()