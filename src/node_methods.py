from textnode import TextNode, TextType
import re
 
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        if old_node.text.count(delimiter) % 2 == 0 and old_node.text.count(delimiter) != 0:
            split_nodes = old_node.text.split(delimiter, 2)
            if len(split_nodes) == 3:
                if split_nodes[0]:
                    new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
                if split_nodes[1]:
                    new_node = TextNode(split_nodes[1], text_type)
                    new_node.is_split = True
                    new_nodes.append(new_node)
                if split_nodes[2]:
                    new_nodes.extend(split_nodes_delimiter([TextNode(split_nodes[2], TextType.TEXT)], delimiter, text_type))
        elif old_node.text.count(delimiter) == 1:
            raise Exception("invalid markdown text")
        elif old_node.is_split == False:
            new_nodes.append(old_node)
            
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if extract_markdown_images(old_node.text) == []:
            new_nodes.append(old_node)
        else:
            image_alt = extract_markdown_images(old_node.text)[0][0]
            image_link = extract_markdown_images(old_node.text)[0][1]
            text_strings = old_node.text.split(f"![{image_alt}]({image_link})", 1)
            if len(text_strings) == 2:
                if text_strings[0]:
                    new_nodes.extend([TextNode(text_strings[0], TextType.TEXT), 
                                    TextNode(image_alt, TextType.IMAGE, image_link)])
                if text_strings[1]:
                    new_nodes.extend(split_nodes_image([TextNode(text_strings[1], TextType.TEXT)]))
            else:
                if text_strings[0]:
                    new_nodes.extend([TextNode(text_strings[0], TextType.TEXT), 
                                    TextNode(image_alt, TextType.IMAGE, image_link)])
    return new_nodes
    
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if extract_markdown_links(old_node.text) == []:
            new_nodes.append(old_node)
        else:
            link_alt = extract_markdown_links(old_node.text)[0][0]
            link_link = extract_markdown_links(old_node.text)[0][1]
            text_strings = old_node.text.split(f"[{link_alt}]({link_link})", 1)
            if len(text_strings) == 2:
                if text_strings[0]:
                    new_nodes.extend([TextNode(text_strings[0], TextType.TEXT), 
                                    TextNode(link_alt, TextType.LINK, link_link)])
                if text_strings[1]:
                    new_nodes.extend(split_nodes_link([TextNode(text_strings[1], TextType.TEXT)]))
            else:
                if text_strings[0]:
                    new_nodes.extend([TextNode(text_strings[0], TextType.TEXT), 
                                    TextNode(link_alt, TextType.LINK, link_link)])
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes