from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # returns list of new_nodes based on where delimiter
    # is found in the code (w/ matching)
    # Converts a Text type to passed in text_type based on delimiter
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
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


def extract_markdown_images(text):
    returner = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    print(returner)
    return returner
