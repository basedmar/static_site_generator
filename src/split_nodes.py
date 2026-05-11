from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        splitted = node.text.split(sep=delimiter)
        if len(splitted) % 2 == 0:
            raise Exception("string is not in proper markdown format")
        
        new_nodes.extend(turn_into_node(splitted, text_type))

    return new_nodes


def turn_into_node(split, delim_type):
    whole = []
    for i, text in enumerate(split):
        if text == "":
            continue
        if i % 2 == 0:
            whole.append(Textnode(text, TextType.TEXT))
        else:
            whole.append(Textnode(text, delim_type))
    return whole

