import re
from enum import Enum
from htmlnode import LeafNode
from parse_markdown import extract_markdown_images, extract_markdown_links


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        if (self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url):
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"


def text_node_to_html_node(text_node) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT: 
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("invalid URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("invalid URL")
            return LeafNode("img", None, props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("textNodes must have a text_type")


def split_text_nodes(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes= []
    # match delimiter:
    #     case "**":
    #         text_type = TextType.BOLD
    #     case "_":
    #         text_type = TextType.ITALIC
    #     case "`":
    #         text_type = TextType.CODE
    #     case _:
    #         raise Exception("invalid delimiter")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 != 1:
                raise Exception("unmatched delimiter")
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i % 2 == 0:
                    text_node = TextNode(split_text[i], TextType.TEXT)
                else:
                    text_node = TextNode(split_text[i], text_type)
                new_nodes.append(text_node)

    return new_nodes


def split_image_nodes(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes= []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        match_idx = 0
        split_text = re.split(r"!\[(.*?)\)", node.text)
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                text_node = TextNode(split_text[i], TextType.TEXT)
            else:
                text_node = TextNode(
                    matches[match_idx][0], 
                    TextType.IMAGE, 
                    matches[match_idx][1]
                )
                match_idx += 1
            new_nodes.append(text_node)

    return new_nodes


def split_link_nodes(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes= []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        match_idx = 0
        split_text = re.split(r"(?<!!)\[(.*?)\)", node.text)
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                text_node = TextNode(split_text[i], TextType.TEXT)
            else:
                text_node = TextNode(
                    matches[match_idx][0], 
                    TextType.LINK, 
                    matches[match_idx][1]
                )
                match_idx += 1
            new_nodes.append(text_node)

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    text_node = TextNode(text, TextType.TEXT)
    # BOLD
    nodes = split_text_nodes([text_node], "**", TextType.BOLD)
    # ITALIC
    nodes = split_text_nodes(nodes, "_", TextType.ITALIC)
    # CODE
    nodes = split_text_nodes(nodes, "`", TextType.CODE)
    # IMAGE
    nodes = split_image_nodes(nodes)
    # LINKS
    nodes = split_link_nodes(nodes)
    return nodes

