import unittest
from htmlnode import HTMLNode

class TestMTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode(
            "div",
            "Lorem ipsum",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "Lorem ipsum",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_both_val_and_children_cantbe_null(self):
        with self.assertRaises(ValueError):
            HTMLNode("h1", props= {
            "id": "abc",
            "className": "class",
            })

    def test_repr_nochildren(self):
        node = HTMLNode("h1", "Heading", props= {
            "id": "abc",
            "className": "class",
        })

        expected = """
        HTMLNode(tag: h1, value: Heading ,
        children: None , 
        props: {'id': 'abc', 'className': 'class'}
        """

        self.assertEqual(
            repr(node), expected
        )
    
    def test_repr(self):
        child1 = HTMLNode("h2", "Sub Heading", props= {
            "id": "abcd",
            "className": "class",
        })
        child2 = HTMLNode("h2", "Sub Heading", props= {
            "id": "abcde",
            "className": "class",
        })
        node = HTMLNode("h1", "Heading", 
            [child1, child2],
            {
                "id": "abc",
                "className": "class",
            })

        expected = """
        HTMLNode(tag: h1, value: Heading ,
        children: [
        HTMLNode(tag: h2, value: Sub Heading ,
        children: None , 
        props: {'id': 'abcd', 'className': 'class'}
        , 
        HTMLNode(tag: h2, value: Sub Heading ,
        children: None , 
        props: {'id': 'abcde', 'className': 'class'}
        ] , 
        props: {'id': 'abc', 'className': 'class'}
        """

        self.assertEqual(
            repr(node), expected
        )
    
    def test_props_to_html(self):
        node = HTMLNode("h1", "Heading", None, {
            "id": "abc",
            "className": "class",
        })

        expected = ' id="abc" className="class"'

        self.assertEqual(
            node.props_to_html(), expected
        )
    

if __name__ == "__main__":
    unittest.main()