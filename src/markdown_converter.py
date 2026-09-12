from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        new_text = node.text.split(delimiter)

        if len(new_text) % 2 == 0:
            raise ValueError(f"Incorrect markdown formatting: {delimiter} section not closed")

        split_nodes = []

        for i in range(len(new_text)):
            if new_text[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(new_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(new_text[i], text_type))
        new_nodes.extend(split_nodes)
            
    return new_nodes

def extract_markdown_images(text) -> list[tuple]:
    matches = re.findall(r"!\[([^\(\)]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[([^\(\)]*)\]\(([^\(\)]*)\)",text)
    return matches