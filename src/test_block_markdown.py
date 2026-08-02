import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a unordered list
- with items
"""

        blocks = markdown_to_blocks(md)

        self.assertListEqual(
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a unordered list\n- with items",
        ],
        blocks,
        )

    def test_markdown_to_blocks_with_empty_block(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is a paragraph before the empty block

"""

        blocks = markdown_to_blocks(md)

        self.assertListEqual(
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is a paragraph before the empty block",
        ],
        blocks,
        )

    def test_block_to_block_type_heading(self):
        block = """# Heading level 1
## Heading level 2
##### Heading level 5
###### Heading level 6"""

        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING_BLOCK, block_type)

    def test_block_to_block_type_code(self):
        block = """```
{
  "json": true,
  "field": "value",
}
```"""

        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE_BLOCK, block_type)

    def test_block_to_block_type_quote(self):
        block = """> Blockquote example
> Another blockquote example"""

        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE_BLOCK, block_type)

    def test_block_to_block_type_unordered_list(self):
        block = """- Unordered list element a
- element b
- element c"""

        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST_BLOCK, block_type)

    def test_block_to_block_type_ordered_list(self):
        block = """1. Ordered list element 1
2. element 2
3. element 3"""

        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST_BLOCK, block_type)

    def test_block_to_block_type_paragraph(self):
        block = """Paragraph block
Second line
Third line"""

        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH_BLOCK, block_type)
    


if __name__ == "__main__":
    unittest.main()