import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\"target=\"_blank\"")
        
    def test_tag(self):
        node = HTMLNode(tag="p")
        node2 = HTMLNode(tag="p")
        self.assertEqual(node.tag, node2.tag)
    
    def test_value(self):
        node = HTMLNode(value="ballin")
        node2 = HTMLNode(value="ballin")
        self.assertEqual(node.value, node2.value)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandparent(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode("span", [child_node])
        grandparent_node = ParentNode("div", [parent_node])
        self.assertEqual(
            grandparent_node.to_html(),
            "<div><span><b>child</b></span></div>",
        )
        
    def test_to_html_2_children(self):
        child_node = LeafNode("b", "child")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("span", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(),
                         "<span><b>child</b><b>child2</b></span>")
        
    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("span", None)
            parent_node.to_html()
        
if __name__ == "__main__":
    unittest.main()