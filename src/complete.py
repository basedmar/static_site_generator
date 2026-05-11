from convert_markdown import *
from extract_links import *
from htmlnode import *
from textnode import *

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlnodes = []
    for block in blocks:
        block_type = block_to_block_type(block)        
        if block_type.value == "paragraph":
            block = block.replace("\n", " ")
            text_nodes = text_to_textnode(block)
            nodes = []
            for node in text_nodes:
                print(node.text)
                print("---")
                nodes.append(text_node_to_html_node(node))
            htmlnodes.append(ParentNode("p", nodes))

        elif block_type.value == "heading":
            count = 0
            for x in range(len(block)):
                if block[x] == "#":
                    count += 1
                else:
                    break
            block = block[count:]
            block = block.lstrip()
            block = block.replace("\n", " ")
            text_nodes = text_to_textnode(block)
            nodes = []
            for node in text_nodes:
                nodes.append(text_node_to_html_node(node))
            htmlnodes.append(ParentNode(f"h{count}", nodes))

        elif block_type.value == "code":
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            text = block[4:-3]
            text_node = Textnode(text, TextType.TEXT)
            text_node = text_node_to_html_node(text_node)
            inner = ParentNode("code", [text_node])
            output = ParentNode("pre", [inner])
            htmlnodes.append(output)

        elif block_type.value == "quote":
            split = block.split("\n")
            for i in range(0,len(split)):
                split[i] = split[i] = split[i][1:].lstrip()
            split = " ".join(split)
            text_nodes = text_to_textnode(split)
            nodes = []
            for node in text_nodes:
                nodes.append(text_node_to_html_node(node))
            htmlnodes.append(ParentNode("blockquote", nodes))

        elif block_type.value == "unordered list":
            split = block.split("\n")
            for i in range(0,len(split)):
                split[i] = split[i][2:]
            text_nodes = []
            for item in split:
                output = text_to_textnode(item)
                text_nodes.append(output)
            subs = []
            for node in text_nodes:
                nodes = []
                for line in node:
                    b = text_node_to_html_node(line)
                    nodes.append(b)
            
                subs.append(ParentNode("li", nodes))
            htmlnodes.append(ParentNode("ul", subs))
            
        elif block_type.value == "Ordered list":
            split = block.split("\n")
            for i in range(0,len(split)):
                split[i] = split[i][len(f"{i + 1}. "):]
            text_nodes = []
            for item in split:
                text_nodes.append(text_to_textnode(item))
            subs = []
            for node in text_nodes:
                nodes = []
                for line in node:
                    b = text_node_to_html_node(line)
                    nodes.append(b)
            
                subs.append(ParentNode("li", nodes))
            htmlnodes.append(ParentNode("ol", subs))
    
    x = ParentNode("html", htmlnodes)
    return x
