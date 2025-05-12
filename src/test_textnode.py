import unittest

from textnode import TextNode, TextType
from node_methods import *
from markdown_methods import *


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
        node = TextNode("This is text with a `code block` word or `two`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT, None), 
                                     TextNode("code block", TextType.CODE, None), 
                                     TextNode(" word or ", TextType.TEXT, None),
                                     TextNode("two", TextType.CODE)])

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) or two ![image2](test.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "test.com")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) or two [link2](hehe.haha)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "hehe.haha")], matches)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                        TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),
                              TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                              TextNode(" and another ", TextType.TEXT),
                              TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")],
                             new_nodes)
        
    def test_split_links(self):
        node = TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
                        TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with a ", TextType.TEXT),
                              TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                              TextNode(" and another ", TextType.TEXT),
                              TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")],
                             new_nodes)
        
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual([TextNode("This is ", TextType.TEXT),
                              TextNode("text", TextType.BOLD),
                              TextNode(" with an ", TextType.TEXT),
                              TextNode("italic", TextType.ITALIC),
                              TextNode(" word and a ", TextType.TEXT),
                              TextNode("code block", TextType.CODE),
                              TextNode(" and an ", TextType.TEXT),
                              TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                              TextNode(" and a ", TextType.TEXT),
                              TextNode("link", TextType.LINK, "https://boot.dev")],
                             text_to_textnodes(text))
        
    def test_text_to_textnode2(self):
        text = "This is **text** with a `code block` and a `code block`"
        self.assertListEqual([TextNode("This is ", TextType.TEXT),
                              TextNode("text", TextType.BOLD),
                              TextNode(" with a ", TextType.TEXT),
                              TextNode("code block", TextType.CODE),
                              TextNode(" and a ", TextType.TEXT),
                              TextNode("code block", TextType.CODE)],
                             text_to_textnodes(text))

    def test_text_to_textnode3(self):
        text = "This is **text** with a `code block` and a `code block` and a `code block` and a `code block` and a `code block`"
        self.assertListEqual([TextNode("This is ", TextType.TEXT),
                              TextNode("text", TextType.BOLD),
                              TextNode(" with a ", TextType.TEXT),
                              TextNode("code block", TextType.CODE),
                              TextNode(" and a ", TextType.TEXT),
                              TextNode("code block", TextType.CODE),
                              TextNode(" and a ", TextType.TEXT),
                              TextNode("code block", TextType.CODE),
                              TextNode(" and a ", TextType.TEXT),
                              TextNode("code block", TextType.CODE),
                              TextNode(" and a ", TextType.TEXT),
                              TextNode("code block", TextType.CODE)],
                             text_to_textnodes(text))
        
    
if __name__ == "__main__":
    unittest.main()