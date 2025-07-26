from textnode import TextNode, TextType, BlockType
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
    print(f"node before: {node}")
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    print(f"node bold: {node}")
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    print(f"node italic: {node}")
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    print(f"node code: {node}")
    node = split_nodes_image(node)
    print(f"node image: {node}")
    node = split_nodes_link(node)
    print(f"node link: {node}")
    return node


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for b in blocks:
        b = b.strip(" ")
        b = b.strip("\n")
        if b == "":
            del b
        new_blocks.append(b)
    return new_blocks


def block_to_block_type(block):
    if re.search(r"^#+\s+", block, re.M) is not None:
        return BlockType.HEADING
    if re.search(r"^`{3}(?s:.*)`{3}", block, re.M) is not None:
        return BlockType.CODE
    if re.search(r"\"(.*?)\"", block, re.M) is not None:
        return BlockType.QUOTE
    if block[0][0] == "-":
        return BlockType.UNORDERED_LIST
    if block[0][0] == "1.":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
