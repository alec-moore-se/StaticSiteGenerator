from enum import Enum
from htmlnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and \
            self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})\n"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "",
                        {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Not a valid text type")


class TextType(Enum):
    TEXT = ""
    BOLD = "<b></b>"
    ITALIC = "<i></i>"
    CODE = "<code></code>"
    LINK = "<a href=></a>"
    IMAGE = "<img src= alt= />"


class BlockType(Enum):
    PARAGRAPH = ""
    HEADING = "#"
    CODE = "`"
    QUOTE = '"'
    UNORDERED_LIST = "-"
    ORDERED_LIST = "$"
