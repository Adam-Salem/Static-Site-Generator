from enum import Enum
from htmlnode import ParentNode, LeafNode, HTMLNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return (self.text == other.text and 
        self.text_type == other.text_type and 
        self.url == other.url)
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def text_node_to_html_node(self):
        if (self.text_type == TextType.TEXT):
            return LeafNode(tag=None,value=self.text)
        if (self.text_type == TextType.BOLD):
            return LeafNode(tag="b",value=self.text)
        if (self.text_type == TextType.ITALIC):
            return LeafNode(tag="i",value=self.text)
        if (self.text_type == TextType.CODE):
            return LeafNode(tag="code",value=self.text)
        if (self.text_type == TextType.LINK):
            return LeafNode(tag="a",value=self.text, props={"href"})
        if (self.text_type == TextType.IMAGE):
            return LeafNode(tag="img",value="",props={"src","alt"})
        
