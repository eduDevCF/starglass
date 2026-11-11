import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode


class BlockType(Enum):
    P = "p"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    CODE = "code"
    QUOTE = "blockquote"
    UL = "ul"
    OL = "ol"


def extract_code_blocks(text: str) -> list[str]:
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
    code_blocks: list[str] = extract_code_blocks(text.lstrip())

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


def markdown_to_html_node(markdown: str) -> ParentNode:
    
    html_block_nodes = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        blocktype = block_to_block_type(block)
        text = strip_md(blocktype, block)

        # CODE block is handled differently for its formatting: <pre><code></code></pre>
        if blocktype == BlockType.CODE:
            html_block_nodes.append(ParentNode("pre", [LeafNode("code", text)]))
            continue

        # OLs and ULs are handled differently: <ol><li></li><li></li></ol>
        if blocktype == BlockType.OL or blocktype == BlockType.UL:
            if blocktype == BlockType.OL:
                toss, *split_list = re.split(r"\d. ", text)
            if blocktype == BlockType.UL:
                toss, *split_list = re.split(r"- ", text)
            li_nodes = []
            for item in split_list:
                children: list[HTMLNode] = text_to_children(item)
                if len(children) > 0:
                    li_nodes.append(ParentNode("li", children))
            if len(li_nodes) > 0:
                html_block_nodes.append(ParentNode(blocktype.value, li_nodes))
            continue
        
        # All other blocks are more straightforward
        children: list[HTMLNode] = text_to_children(text)
        if len(children) > 0:
            html_block_nodes.append(ParentNode(blocktype.value, children))

    return ParentNode("div", html_block_nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    from textnode import text_to_text_nodes, text_node_to_html_node
    # OL and UL list items need this check
    if text[-1] == "\n":
        text = text[:-1]

    child_nodes: list = []
    text_nodes: list[textnode] = text_to_text_nodes(text)
    for text_node in text_nodes:
        child_nodes.append(text_node_to_html_node(text_node))
    return child_nodes


def strip_md(blocktype: BlockType, text: str) -> str:
    text = text.strip()
    match blocktype:
        case BlockType.P:
            text = text.replace("\n", " ")
            return text
        case BlockType.H6:
            return text[7:]
        case BlockType.H5:
            return text[6:]
        case BlockType.H4:
            return text[5:]
        case BlockType.H3:
            return text[4:]
        case BlockType.H2:
            return text[3:]
        case BlockType.H1:
            return text[2:]
        case BlockType.CODE:
            text = text.rstrip()
            return text[4:]
        case BlockType.QUOTE:
            return text[1:].lstrip()
        case BlockType.UL:
            return text
        case BlockType.OL:
            return text

