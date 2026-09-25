import re
from enum import Enum

class BlockType(Enum):
    P = "paragraph"
    H1 = "heading1"
    H2 = "heading2"
    H3 = "heading3"
    H4 = "heading4"
    H5 = "heading5"
    H6 = "heading6"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered list"
    OL = "ordered list"


def extract_code_blocks(text: str) -> list[str]:
    #Todo: Write tests
    blocks = []
    code_blocks = text.split("```")

    for i in range(len(code_blocks)):
        if code_blocks[i] == "":
            continue
        if i % 2 == 1:
            code_block = "```" + code_blocks[i]
            blocks.append(code_block)
        if i % 2 == 0:
            blocks.append(code_blocks[i])
    
    return blocks


def markdown_to_blocks(text: str) -> list[str]:
    #Todo: UPDATE TESTS to include code blocks
    code_blocks: list[str] = extract_code_blocks(text)

    blocks = []
    for item in code_blocks:
        if item[0:4] == "```\n":
            blocks.append(item)
        else:
            text_blocks = item.split("\n\n")
            for block in text_blocks:
                polished_block = block.strip()
                if polished_block == "":
                    continue
                blocks.append(polished_block)

    return blocks


def block_to_block_type(text: str) -> BlockType:
    # Todo: write tests
    if text.startswith("###### "):
        return BlockType.H6
    if text.startswith("##### "):
        return BlockType.H5
    if text.startswith("#### "):
        return BlockType.H4
    if text.startswith("### "):
        return BlockType.H3
    if text.startswith("## "):
        return BlockType.H2
    if text.startswith("# "):
        return BlockType.H1
    if text.startswith("```\n"):
        return BlockType.CODE
    if text.startswith(">"):
        return BlockType.QUOTE
    if text.startswith("- "):
        return BlockType.UL
    if re.match(r"(\d. )", text):
        return BlockType.OL
    return BlockType.P


def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    

def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


