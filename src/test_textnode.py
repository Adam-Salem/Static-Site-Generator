import unittest

from textnode import TextNode, TextType
from node_methods import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_neq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.website.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.website.com")
        self.assertEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.website.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
        
    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href"})
        self.assertEqual(html_node.value, "This is a link text node")
        
    def test_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src", "alt"})
        self.assertEqual(html_node.value, "")
        
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT, None), 
                                     TextNode("code block", TextType.CODE, None), 
                                     TextNode(" word", TextType.TEXT, None)])

    def test_split_multiple_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT, None), 
                                     TextNode("code block", TextType.CODE, None), 
                                     TextNode(" word", TextType.TEXT, None),
                                     TextNode("This is text with an _italic_ word", TextType.TEXT)])

    def test_split_multiple_nodes2(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with a `code block` word", TextType.TEXT),
                                     TextNode("This is text with an ", TextType.TEXT),
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" word", TextType.TEXT)])

    def test_split_multiple_nodes3(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with another `code` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT, None), 
                                     TextNode("code block", TextType.CODE, None), 
                                     TextNode(" word", TextType.TEXT, None),
                                     TextNode("This is text with another ", TextType.TEXT),
                                     TextNode("code", TextType.CODE),
                                     TextNode(" word", TextType.TEXT)])

    def test_split_nodes_wrong_type(self):
        node = TextNode("This is text with a `code` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with a `code` word", TextType.TEXT)])

    def test_split_nodes_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT, None), 
                                     TextNode("bold", TextType.BOLD, None), 
                                     TextNode(" word", TextType.TEXT, None)])

if __name__ == "__main__":
    unittest.main()