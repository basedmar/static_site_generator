import re
from textnode import *
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        plain = node.text
        regex = extract_markdown_images(plain)
        if len(regex) == 0:
            new_nodes.append(node)
            continue
        for pic in regex:
            string = plain.split(f"![{pic[0]}]({pic[1]})", maxsplit=1)
            if len(string) != 2:
                raise Exception("not proper markdown")
            if string[0] != "":
                new_nodes.append(Textnode(string[0], TextType.TEXT))
            new_nodes.append(Textnode(pic[0], TextType.IMAGE, pic[1]))
            plain = string[1]
        if plain != "":
             new_nodes.append(Textnode(plain, TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        plain = node.text
        regex = extract_markdown_links(plain)
        if len(regex) == 0:
            new_nodes.append(node)
            continue
        for pic in regex:
            string = plain.split(f"[{pic[0]}]({pic[1]})", maxsplit=1)
            if len(string) != 2:
                raise Exception("not proper markdown")
            if string[0] != "":
                new_nodes.append(Textnode(string[0], TextType.TEXT))
            new_nodes.append(Textnode(pic[0], TextType.LINK, pic[1]))
            plain = string[1]
        if plain != "":
            new_nodes.append(Textnode(plain, TextType.TEXT))
    return new_nodes