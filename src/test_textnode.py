import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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


if __name__ == "__main__":
    unittest.main()