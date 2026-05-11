from textnode import *
from split_nodes import *
from extract_links import *
from enum import Enum
def text_to_textnode(text):
    inital = Textnode(text, TextType.TEXT)
    bold = split_nodes_delimiter([inital], "**", TextType.BOLD_TEXT)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC_TEXT)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    image = split_nodes_images(code)
    links = split_nodes_links(image)
    return links
    
def markdown_to_blocks(markdown):
    blocks = []
    markdown = markdown.strip()
    splitted = markdown.split("\n\n")
    for block in splitted:
        blocks.append(block.strip())
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "Ordered list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    

    


