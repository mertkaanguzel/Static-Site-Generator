import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_with_children(self):
        child1 = LeafNode("h2", "Sub Heading 1", props= {
            "id": "abcd",
            "className": "class",
        })
        child2 = LeafNode("h2", "Sub Heading 2", props= {
            "id": "abcde",
            "className": "class",
        })
        node = ParentNode("h1", 
            [child1, child2],
            {
                "id": "abc",
                "className": "class",
            })

        expected = '<h1 id="abc" className="class"><h2 id="abcd" className="class">Sub Heading 1</h2><h2 id="abcde" className="class">Sub Heading 2</h2></h1>'

        self.assertEqual(
            node.to_html(), expected
        )

    def test_parent_to_html_with_grandchildren(self):
        child3 = LeafNode("h3", "Sub Heading 2", props= {
            "id": "abcdef",
            "className": "class",
        })
        child1 = ParentNode("div", 
            [child3],
            {
                "id": "abcd",
                "className": "class",
            })
        child2 = LeafNode("h2", "Sub Heading 1", props= {
            "id": "abcde",
            "className": "class",
        })
        node = ParentNode("h1", 
            [child1, child2],
            {
                "id": "abc",
                "className": "class",
            })

        expected = '<h1 id="abc" className="class"><div id="abcd" className="class"><h3 id="abcdef" className="class">Sub Heading 2</h3></div><h2 id="abcde" className="class">Sub Heading 1</h2></h1>'

        self.assertEqual(
            node.to_html(), expected
        )

    def test_to_html_with_grandchildren_2(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode(None, "grandchild2")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node])

        expected = "<div><span><b>grandchild</b>grandchild2</span></div>"

        self.assertEqual(
            parent_node.to_html(),
            expected,
        )

    def test_parent_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            child1 = LeafNode("h2", "Sub Heading 1")
            node = ParentNode("", [child1])
            node.to_html()

    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("", [])
            node.to_html()

    def test_repr(self):
        child_node = LeafNode(None, "span")
        node = ParentNode("div", [child_node], {
                "id": "abc",
                "className": "class",
            })

        expected = """
        ParentNode(tag: div ,
        children: [
        LeafNode(tag: None, value: span ,
        props: None
        ] , 
        props: {'id': 'abc', 'className': 'class'}
        """

        self.assertEqual(
            repr(node), expected
        )
    

if __name__ == "__main__":
    unittest.main()