import re

def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def markdown_to_blocks(text: str) -> list[str]:
    raw_blocks = text.split("\n\n")
    blocks = []
    for block in raw_blocks:
        polished_block = block.strip()
        if polished_block == "":
            continue
        blocks.append(block)
    return blocks

