from textnode import TextNode, TextType
 
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        if old_node.text.count(delimiter) == 2:
            split_nodes = old_node.text.split(delimiter)
            for i in range(len(split_nodes)):
                if i == 1:
                    new_nodes.append(TextNode(split_nodes[i], text_type))
                else:
                    new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
        elif old_node.text.count(delimiter) == 1:
            raise Exception("invalid markdown text")
        else:
            new_nodes.append(old_node)
    return new_nodes