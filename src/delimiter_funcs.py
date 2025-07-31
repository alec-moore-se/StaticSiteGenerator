from textnode import TextNode, TextType, BlockType, text_node_to_html_node
from htmlnode import ParentNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # returns list of new_nodes based on where delimiter
    # is found in the code (w/ matching)
    # Converts a Text type to passed in text_type based on delimiter
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parsing_node = node.text
        if delimiter != "":
            parsing_node = node.text.split(delimiter)
        if len(parsing_node) % 2 != 1:
            raise Exception("no matching markdown syntax")
        for i in range(len(parsing_node)):
            if i % 2 == 0:
                new_nodes.append(TextNode(parsing_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parsing_node[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
        else:
            for im in images:
                working_node = node.text.split(f"![{im[0]}]({im[1]})", 1)
                if working_node[0] != "":
                    new_nodes.append(TextNode(working_node[0], TextType.TEXT))
                new_nodes.append(TextNode(im[0], TextType.IMAGE, im[1]))
                node.text = working_node[1]
            if node.text != "":
                new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    working_node = None
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
        else:
            for im in links:
                working_node = node.text.split(f"[{im[0]}]({im[1]})", 1)
                if working_node[0] != "":
                    new_nodes.append(TextNode(working_node[0], TextType.TEXT))
                new_nodes.append(TextNode(im[0], TextType.LINK, im[1]))
                node.text = working_node[1]
            if node.text != "":
                new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    # Pulls links from a text block, stores in a tuple list
    # [(alt text, link)]
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    # Pulls links from a text block, stores in a tuple list
    # [(display_text, link)]
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def text_to_textnodes(text):
    # text is a single string
    node = [TextNode(text, TextType.TEXT)]
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for b in blocks:
        b = b.strip()
        if b == "":
            continue
        new_blocks.append(b)
    return new_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    if re.search(r"^#+\s+", block, re.M) is not None:
        return BlockType.HEADING
    if re.search(r"^`{3}(?s:.*)`{3}", block, re.M) is not None:
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
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def extract_title(markdown):
    list_of_finds = re.findall(r"\s*?#{1} (.*?)$", markdown, re.M)
    if list_of_finds == []:
        raise Exception("No main header, needed for title")
    title = list_of_finds[0]
    title.strip()
    title.lstrip("# ")
    return title
