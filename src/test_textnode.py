import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_text_nodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_type_eq(self):
        node = TextNode("This text is code", TextType.CODE)
        node2 = TextNode("This code is a text node", TextType.CODE)
        self.assertEqual(node.text_type, node2.text_type)
    
    def test_url_is_none(self):
        node = TextNode("This is just plain", TextType.TEXT)
        self.assertEqual(node.url, None)
    
    def test_url_not_none(self):
        node = TextNode("This is a link", TextType.LINK, "http://boot.dev")
        self.assertNotEqual(node.url, None)
    
    def test_image_type_equal(self):
        node = TextNode("This is img alt text", TextType.IMAGE, "test.gif")
        node2 = TextNode("This is different alt text", TextType.IMAGE, "test2.gif")
        self.assertEqual(node.text_type, node2.text_type)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")
    
    def test_italics(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is a italic text node</i>")
    
    def test_code(self):
        node = TextNode("This text node is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This text node is code</code>")

    def test_link(self):
        node = TextNode("Click this link", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="https://boot.dev">Click this link</a>')
    
    def test_image(self):
        node = TextNode("image alt text", TextType.IMAGE, "img.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="img.jpg" alt="image alt text">')

    def test_inline_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_text_nodes([node], "`", TextType.CODE)
        test_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_multiple_delimiters(self):
        node = TextNode("How to use `if`, `elif`, and `else` statements", TextType.TEXT)
        new_nodes = split_text_nodes([node], "`", TextType.CODE)
        test_nodes = [
            TextNode("How to use ", TextType.TEXT),
            TextNode("if", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("elif", TextType.CODE),
            TextNode(", and ", TextType.TEXT),
            TextNode("else", TextType.CODE),
            TextNode(" statements", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_delimiter_at_start_and_end(self):
        node = TextNode("**THE END**", TextType.TEXT)
        new_nodes = split_text_nodes([node], "**", TextType.BOLD)
        test_nodes = [TextNode("THE END", TextType.BOLD)]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_multiple_nodes(self):
        node1 = TextNode("Nobody:", TextType.TEXT)
        node2 = TextNode("Tall People: _touches ceiling_", TextType.TEXT)
        node3 = TextNode("Short People: _rolls eyes_", TextType.TEXT)
        new_nodes = split_text_nodes([node1, node2, node3], "_", TextType.ITALIC)
        test_nodes = [
            TextNode("Nobody:", TextType.TEXT),
            TextNode("Tall People: ", TextType.TEXT),
            TextNode("touches ceiling", TextType.ITALIC),
            TextNode("Short People: ", TextType.TEXT),
            TextNode("rolls eyes", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, test_nodes)
    
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_text_nodes([node], "**", TextType.BOLD)
        new_nodes = split_text_nodes(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()