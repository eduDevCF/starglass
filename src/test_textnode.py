import unittest
from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()