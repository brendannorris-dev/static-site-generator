from markdown_converter import markdown_to_blocks, text_to_textnodes
from blocktype import block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType

def markdown_to_html_node(markdown):
    new_markdown = markdown_to_blocks(markdown)

    markdown_blocks = []
    for individual_block in new_markdown:
        #Determine the block type for each block
        ib_block_type = block_to_block_type(individual_block)

        #Create HTML Node based on type of block
        if ib_block_type == BlockType.PARAGRAPH:
            individual_block = individual_block.replace("\n", " ")
            children_block = text_to_children(individual_block)
            new_node = ParentNode("p", children_block)

        elif ib_block_type == BlockType.QUOTE:
            clean_quote = individual_block.split("\n")
            clean_quote_list = []
            for line in clean_quote:
                if line.startswith(">"):
                    line = line[1:]
                if line.startswith(" "):
                    line = line[1:]
                clean_quote_list.append(line)
            rejoined_quote = " ".join(clean_quote_list)
            children_block = text_to_children(rejoined_quote)
            new_node = ParentNode("blockquote", children_block)

        elif ib_block_type == BlockType.UNORDERED_LIST:
            clean_uo = individual_block.split("\n")
            clean_uo_list = []
            for line in clean_uo:
                line = line[2:]
                line_list = text_to_children(line)
                line_node = ParentNode("li", line_list)
                clean_uo_list.append(line_node)
            new_node = ParentNode("ul", clean_uo_list)

        elif ib_block_type == BlockType.ORDERED_LIST:
            clean_o = individual_block.split("\n")
            clean_o_list = []
            for line in clean_o:
                period_index = line.find(".")
                line = line[(period_index)+2:]
                line_list = text_to_children(line)
                line_node = ParentNode("li",line_list)
                clean_o_list.append(line_node)
            new_node = ParentNode("ol", clean_o_list)

        elif ib_block_type == BlockType.CODE:
            individual_block = individual_block[4:-3]
            new_ib = TextNode(individual_block, TextType.TEXT)
            new_leaf = text_node_to_html_node(new_ib)
            middle_parent = ParentNode("code", [new_leaf])
            new_node = ParentNode("pre", [middle_parent])

        elif ib_block_type == BlockType.HEADING:
            count = 0
            for letter in individual_block:
                if letter == "#":
                    count += 1
                    continue
                else:
                    break
            individual_block = individual_block[count+1:]
            new_ib = text_to_children(individual_block)
            new_node = ParentNode(f"h{count}", new_ib)
            
        markdown_blocks.append(new_node)

    main_parent = ParentNode("div", markdown_blocks)

    return main_parent

def text_to_children(text):
    children_list = text_to_textnodes(text)
    html_list = []
    for child in children_list:
        new_child = text_node_to_html_node(child)
        html_list.append(new_child)
    return html_list