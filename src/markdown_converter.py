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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})",1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1]
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes    

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})",1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_node = split_nodes_delimiter(new_node, "_", TextType.ITALIC)
    new_node = split_nodes_delimiter(new_node, "`", TextType.CODE)
    new_node = split_nodes_link(new_node)
    new_node = split_nodes_image(new_node)
    return new_node

def markdown_to_blocks(markdown) -> list[str]:
    blocks = markdown.split("\n\n")
    new_markdown = []
    for line in blocks:
        line = line.strip()
        if line != "":
            new_markdown.append(line)
    return new_markdown

def extract_title(markdown):
    lines_list = markdown.split("\n")
    for line in lines_list:
        if line.startswith("# "):
            return (line[1:].strip())
    raise Exception("Title missing; no line with singular # header")