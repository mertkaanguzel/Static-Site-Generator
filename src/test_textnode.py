import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_PLAIN_TEXT(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_BOLD_TEXT(self):
        node = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_ITALIC_TEXT(self):
        node = TextNode("This is a italic text node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_CODE_TEXT(self):
        node = TextNode("This is a code text node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_LINK_TEXT(self):
        node = TextNode("This is a link text node", TextType.LINK_TEXT, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props.get("href") if html_node.props else "", "https://example.com")
        self.assertEqual(html_node.props, { "href": "https://example.com" })

    def test_LINK_TEXT_WITHOUT_URL(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a link text node", TextType.LINK_TEXT, )
            text_node_to_html_node(node)

    def test_IMAGE_TEXT(self):
        node = TextNode("This is a image text node", TextType.IMAGE_TEXT, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, { "src": "https://example.com", "alt": "This is a image text node" })

    def test_IMAGE_TEXT_WITHOUT_URL(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a link text node", TextType.IMAGE_TEXT, )
            text_node_to_html_node(node)

    

    
                        

                        

if __name__ == "__main__":
    unittest.main()