import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_empty_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", "")
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click", {"href": "https://www.example.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.example.com">Click</a>',
        )

    def test_repr(self):
        node = LeafNode("p", "Hello, world!", props= {
            "id": "abc",
            "className": "class",
        })

        expected = """
        LeafNode(tag: p, value: Hello, world! ,
        props: {'id': 'abc', 'className': 'class'}
        """

        self.assertEqual(
            repr(node), expected
        )
    

if __name__ == "__main__":
    unittest.main()