import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delim_PLAIN_TEXT_ONLY(self):
        node = TextNode("This is an only plain text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        expected_nodes = [
            TextNode("This is an only plain text", TextType.PLAIN_TEXT),
        ]

        self.assertEqual(len(new_nodes), len(expected_nodes))

        for i, node in enumerate(new_nodes):
            self.assertEqual(node, expected_nodes[i])

    def test_delim_CODE_TEXT(self):
        node = TextNode("This is a text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        expected_nodes = [
            TextNode("This is a text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]

        self.assertEqual(len(new_nodes), len(expected_nodes))

        for i, node in enumerate(new_nodes):
            self.assertEqual(node, expected_nodes[i])

    def test_delim_EMPTY_CODE_TEXT(self):
        node = TextNode("This is a text with a `` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        expected_nodes = [
            TextNode("This is a text with a ", TextType.PLAIN_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]

        self.assertEqual(len(new_nodes), len(expected_nodes))

        for i, node in enumerate(new_nodes):
            self.assertEqual(node, expected_nodes[i])
    

    def test_delim_ITALIC_TEXT(self):
        node = TextNode("_This_ is text with an _italic_ word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)

        expected_nodes = [
            TextNode("This", TextType.ITALIC_TEXT),
            TextNode(" is text with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]

        self.assertEqual(len(new_nodes), len(expected_nodes))

        for i, node in enumerate(new_nodes):
            self.assertEqual(node, expected_nodes[i])

    def test_delim_ITALIC_TEXT2(self):
        node = TextNode("_These_ are _texts_ with _italic words_", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)

        expected_nodes = [
            TextNode("These", TextType.ITALIC_TEXT),
            TextNode(" are ", TextType.PLAIN_TEXT),
            TextNode("texts", TextType.ITALIC_TEXT),
            TextNode(" with ", TextType.PLAIN_TEXT),
            TextNode("italic words", TextType.ITALIC_TEXT),
        ]

        self.assertEqual(len(new_nodes), len(expected_nodes))

        for i, node in enumerate(new_nodes):
            self.assertEqual(node, expected_nodes[i])

    def test_delim_BOLD_TEXT(self):
        node = TextNode("**This** is text with a **bold word**", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        expected_nodes = [
            TextNode("This", TextType.BOLD_TEXT),
            TextNode(" is text with a ", TextType.PLAIN_TEXT),
            TextNode("bold word", TextType.BOLD_TEXT),
        ]

        self.assertEqual(len(new_nodes), len(expected_nodes))

        for i, node in enumerate(new_nodes):
            self.assertEqual(node, expected_nodes[i])

    def test_delim_BOLD_TEXT2(self):
        node = TextNode("**This** is text with a **bold** word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        expected_nodes = [
            TextNode("This", TextType.BOLD_TEXT),
            TextNode(" is text with a ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]

        self.assertEqual(len(new_nodes), len(expected_nodes))

        for i, node in enumerate(new_nodes):
            self.assertEqual(node, expected_nodes[i])

    def test_delim_BOLD_TEXT3(self):
        node = TextNode("This is **text** with a **bold** word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        expected_nodes = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with a ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]

        self.assertEqual(len(new_nodes), len(expected_nodes))

        for i, node in enumerate(new_nodes):
            self.assertEqual(node, expected_nodes[i])

    def test_delim_BOLD_and_ITALIC(self):
        node = TextNode("**bold** and _italic_", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![example image](https://www.picsum.photos/536/354)"
        )
        self.assertListEqual([("example image", "https://www.picsum.photos/536/354")], matches)

    def test_extract_markdown_images_multiple(self):
            matches = extract_markdown_images(
                "This is text with a ![example image](https://www.picsum.photos/536/354) and ![example image 2](https://picsum.photos/id/237/200/300)"
            )
            self.assertListEqual([("example image", "https://www.picsum.photos/536/354"), ("example image 2", "https://picsum.photos/id/237/200/300")], matches)

    def test_extract_markdown_links(self):
            matches = extract_markdown_links(
                "This is text with an [example link](https://example.com)"
            )
            self.assertListEqual([("example link", "https://example.com")], matches)

    def test_extract_markdown_link_multiple(self):
        matches = extract_markdown_links(
            "This is text with a [example link](example.com) and [example link 2](https://www.example.com)"
        )
        self.assertListEqual([("example link", "example.com"), ("example link 2", "https://www.example.com")], matches)


if __name__ == "__main__":
    unittest.main()