import unittest

from textnode import *
from htmlnode import *
from split_nodes import *
from extract_links import *
from convert_markdown import *
from complete import *
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = Textnode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = Textnode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = Textnode("This is bold", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestHTMLNode(unittest.TestCase):

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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )



class TESTLEAF(unittest.TestCase):
    def test_text(self):
        node = Textnode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")



class TESTLEAFF(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        print(node.to_html())
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        htmlnode = HTMLNode("p", "hahaha", None, {"href": "https://www.google.com", "hreff": "sigma.com"})
        htmlnode.props_to_htlm()
    def test_repr(self):
        htmlnode = HTMLNode("p", "hahaha", None, {"href": "https://www.google.com", "hreff": "sigma.com"})
        print(htmlnode)

class TestStringsplit(unittest.TestCase):
    print("-------------------------------------------------")
    def test_delim_bold(self):
        node = Textnode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                Textnode("This is text with a ", TextType.TEXT),
                Textnode("bolded", TextType.BOLD_TEXT),
                Textnode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = Textnode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                Textnode("This is text with a ", TextType.TEXT),
                Textnode("bolded", TextType.BOLD_TEXT),
                Textnode(" word and ", TextType.TEXT),
                Textnode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = Textnode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                Textnode("This is text with a ", TextType.TEXT),
                Textnode("bolded word", TextType.BOLD_TEXT),
                Textnode(" and ", TextType.TEXT),
                Textnode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = Textnode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                Textnode("This is text with an ", TextType.TEXT),
                Textnode("italic", TextType.ITALIC_TEXT),
                Textnode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = Textnode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                Textnode("bold", TextType.BOLD_TEXT),
                Textnode(" and ", TextType.TEXT),
                Textnode("italic", TextType.ITALIC_TEXT),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = Textnode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                Textnode("This is text with a ", TextType.TEXT),
                Textnode("code block", TextType.CODE),
                Textnode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    class Testregexlinks(unittest.TestCase):
        def test_extract_markdown_images(self):
            matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_split_image(self):
        node = Textnode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                Textnode("This is text with an ", TextType.TEXT),
                Textnode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = Textnode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                Textnode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = Textnode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                Textnode("This is text with an ", TextType.TEXT),
                Textnode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                Textnode(" and another ", TextType.TEXT),
                Textnode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = Textnode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                Textnode("This is text with a ", TextType.TEXT),
                Textnode("link", TextType.LINK, "https://boot.dev"),
                Textnode(" and ", TextType.TEXT),
                Textnode("another link", TextType.LINK, "https://wikipedia.org"),
                Textnode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    
class Testmarkdownconverter(unittest.TestCase):
    def test_normal(self):
        
        x = text_to_textnode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual([
    Textnode("This is ", TextType.TEXT),
    Textnode("text", TextType.BOLD_TEXT),
    Textnode(" with an ", TextType.TEXT),
    Textnode("italic", TextType.ITALIC_TEXT),
    Textnode(" word and a ", TextType.TEXT),
    Textnode("code block", TextType.CODE),
    Textnode(" and an ", TextType.TEXT),
    Textnode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    Textnode(" and a ", TextType.TEXT),
    Textnode("link", TextType.LINK, "https://boot.dev"),
], x)
        x = text_to_textnode("**text** with an italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) ahaha")
        self.assertListEqual([

            Textnode("text", TextType.BOLD_TEXT),
            Textnode(" with an italic word and a ", TextType.TEXT),
            Textnode("code block", TextType.CODE),
            Textnode(" and an ", TextType.TEXT),
            Textnode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            Textnode(" and a ", TextType.TEXT),
            Textnode("link", TextType.LINK, "https://boot.dev"),
            Textnode(" ahaha", TextType.TEXT)
], x)
        x = text_to_textnode("**text**")
        print(x)
        self.assertListEqual([

            Textnode("text", TextType.BOLD_TEXT),
], x) 
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        md = """


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
lots of items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items\nlots of items",
            ],
        )
        md = """


This is another paragraph with _italic_ text and `code` here


This is the same paragraph on a new line

- This is a list
- with items
lots of items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is another paragraph with _italic_ text and `code` here", "This is the same paragraph on a new line", "- This is a list\n- with items\nlots of items",
            ],
        )
def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
if __name__ == "__main__":
    unittest.main()