import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_eq(self):
        node = HTMLNode("a", "link text", children=None, props={"href": "https://boot.dev"})
        node2 = HTMLNode("a", "link text", children=None, props={"href": "https://boot.dev"})
        self.assertEqual(repr(node), repr(node2))
    
    def test_children(self):
        node = HTMLNode("a", "boot.dev", children=None, props={"href": "https://boot.dev"})
        node2 = HTMLNode("p", "I'm speedrunning ", children=[node], props={"id": "status"})
        self.assertEqual(node, node2.children[0])
        self.assertNotEqual(node, node2)
    
    def test_default_data(self):
        node = HTMLNode("a", "boot.dev", props={"href": "https://boot.dev"})
        node2 = HTMLNode("p", "I'm using Python!")
        node3 = HTMLNode()
        self.assertEqual(node.children, None)
        self.assertEqual(node2.children, None)
        self.assertEqual(node2.props, None)
        self.assertEqual(node3.tag, None)
        self.assertEqual(node3.value, None)


if __name__ == "__main__":
    unittest.main()