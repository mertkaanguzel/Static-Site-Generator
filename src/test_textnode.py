import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_eq_withurl(self):
        node = TextNode("This is a image node", TextType.IMAGE_TEXT, "example.com")
        node2 = TextNode("This is a image node", TextType.IMAGE_TEXT, "example.com")
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node too", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_url(self):
        node = TextNode("This is a image node", TextType.IMAGE_TEXT, "example.com")
        node2 = TextNode("This is a image node", TextType.IMAGE_TEXT, "example1.com")
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a image node", TextType.IMAGE_TEXT, "example.com")
        node2 = TextNode("This is a image node too", TextType.IMAGE_TEXT, "example.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a link node", TextType.LINK_TEXT, "example.com")
        self.assertEqual(
            "TextNode(This is a link node, link, example.com)", repr(node)
        )
    
    def test_repr1(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        self.assertEqual(
            "TextNode(This is a text node, text, None)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()