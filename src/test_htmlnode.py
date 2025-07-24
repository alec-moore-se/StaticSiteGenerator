import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from speed_delimiter import split_nodes_delimiter, extract_markdown_images


class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        hnode1 = HTMLNode("p", "a sentence to test", None, )
        hnode2 = HTMLNode("p", "a sentence to test", None, )
        self.assertEqual(hnode1, hnode2)

    def test_single_prop(self):
        props = {}
        props["href"] = "localhost://8888"
        hnode = HTMLNode(props=props)
        self.assertEqual(hnode.props_to_html(), ' href="localhost://8888"')

    def test_multiple_prop(self):
        props = {}
        props["href"] = "localhost://8888"
        props["bootdev"] = "stylez@bootdev"
        props["target"] = "_other"
        hnode = HTMLNode(props=props)
        self.assertEqual(hnode.props_to_html(
        ), ' href="localhost://8888" bootdev="stylez@bootdev" target="_other"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_ahref(self):
        node = LeafNode("a", "Hello, world!", {"href": "localhost://8888"})
        self.assertEqual(
            node.to_html(), '<a href="localhost://8888">Hello, world!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(),
                         "<code>This is a text node</code>")

    def test_link(self):
        node = TextNode("This is a text node",
                        TextType.LINK, "localhost://8888")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(),
                         "<a href=\"localhost://8888\">This is a text node</a>")

    def test_image(self):
        node = TextNode("This is a text node",
                        TextType.IMAGE, "localhost://8888")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(),
                         "<img src=\"localhost://8888\" alt=\"This is a text node\" />")

    def test_delimter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes_check = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, new_nodes_check)

    def test_delimter_bold(self):
        node = TextNode(
            "This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes_check = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, new_nodes_check)

    def test_delimeter_italic(self):
        node = TextNode(
            "This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes_check = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, new_nodes_check)

    def test_delimeter_text(self):
        new_nodes = []
        node = TextNode(
            "This is text with a text block", TextType.TEXT)
        try:
            new_nodes = split_nodes_delimiter([node], "", TextType.TEXT)
        except Exception:
            pass
        new_nodes_check = [
            TextNode("This is text with a text block", TextType.TEXT)
        ]
        self.assertNotEqual(new_nodes, new_nodes_check)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
