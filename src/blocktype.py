from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block) -> BlockType:
    if block.startswith(('# ','## ','### ','#### ','##### ','###### ')):
        return BlockType.HEADING
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
    block_splits = block.split("\n")
    quote_count=0
    unorder_count=0
    order_count=0
    for i, split_block in enumerate(block_splits):
        if split_block.startswith(">"):
            quote_count += 1
        if split_block.startswith("- "):
            unorder_count += 1
        if split_block.startswith(f"{i+1}. "):
            order_count += 1
    if quote_count == len(block_splits):
        return BlockType.QUOTE
    if unorder_count == len(block_splits):
        return BlockType.UNORDERED_LIST
    if order_count == len(block_splits):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH