from markdown_converter import markdown_to_blocks, text_to_textnodes
from blocktype import block_to_block_type, BlockType
from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []
    for individual_block in blocks:
        #Determine the block type for each block
        ib_block_type = block_to_block_type(individual_block)

        #Create HTML Node based on type of block
        if ib_block_type == BlockType.PARAGRAPH:
            new_node = paragraph_to_node(individual_block)
        elif ib_block_type == BlockType.QUOTE:
            new_node = quote_to_node(individual_block)
        elif ib_block_type == BlockType.UNORDERED_LIST:
            new_node = unordered_list_to_node(individual_block)
        elif ib_block_type == BlockType.ORDERED_LIST:
            new_node = ordered_list_to_node(individual_block)
        elif ib_block_type == BlockType.CODE:
            new_node = code_to_node(individual_block)
        elif ib_block_type == BlockType.HEADING:
            new_node = heading_to_node(individual_block)
            
        block_nodes.append(new_node)

    main_parent = ParentNode("div", block_nodes)

    return main_parent


def text_to_children(text):
    children_list = text_to_textnodes(text)
    html_list = []
    for child in children_list:
        new_child = text_node_to_html_node(child)
        html_list.append(new_child)
    return html_list


def paragraph_to_node(block):
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)


def quote_to_node(block):
    split_quote = block.split("\n")
    quote_list = []
    for line in split_quote:
        new_line = line
        if line.startswith(">"):
            new_line = line[1:]
        if new_line.startswith(" "):
            new_line = new_line[1:]
        quote_list.append(new_line)
    rejoined_quote = " ".join(quote_list)
    children = text_to_children(rejoined_quote)
    return ParentNode("blockquote", children)


def unordered_list_to_node(block):
    split_list = block.split("\n")
    unordered_list = []
    for line in split_list:
        new_line = line[2:]
        children = text_to_children(new_line)
        list_item_node = ParentNode("li", children)
        unordered_list.append(list_item_node)
    return ParentNode("ul", unordered_list)


def ordered_list_to_node(block):
    split_list = block.split("\n")
    ordered_list = []
    for line in split_list:
        period_index = line.find(".")
        trimmed_line = line[(period_index)+2:]
        children = text_to_children(trimmed_line)
        list_item_node = ParentNode("li", children)
        ordered_list.append(list_item_node)
    return ParentNode("ol", ordered_list)


def code_to_node(block):
    trimmed_block = block[4:-3]
    block_node = text_node_to_html_node(TextNode(trimmed_block, TextType.TEXT))
    code_node = ParentNode("code", [block_node])
    return ParentNode("pre", [code_node])


def heading_to_node(block):
    count = 0
    for letter in block:
        if letter == "#":
            count += 1
            continue
        else:
            break
    trimmed_block = block[count+1:]
    children = text_to_children(trimmed_block)
    return ParentNode(f"h{count}", children)