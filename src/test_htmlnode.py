import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


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
