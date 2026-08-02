from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH_BLOCK = "paragraph"
    HEADING_BLOCK = "heading"
    CODE_BLOCK = "code"
    QUOTE_BLOCK = "quote"
    UNORDERED_LIST_BLOCK = "unordered_list"
    ORDERED_LIST_BLOCK = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks: list[str] = []

    for block in blocks:
        if block == "":
            continue
        filtered_blocks.append(block.strip())

    return filtered_blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.splitlines()

    if re.match(r"(#)\1{0,5} ", lines[0]) is not None:
        for i in range(1, len(lines)):
            if not re.match(r"(#)\1{0,5} ", lines[i]):
                break
            if i == len(lines)-1:
                return BlockType.HEADING_BLOCK

    if lines[0] == lines[-1] == "```":
        return BlockType.CODE_BLOCK

    if lines[0].startswith(">"):
        for i in range(1, len(lines)):
            if not lines[i].startswith(">"):
                break
            if i == len(lines)-1:
                return BlockType.QUOTE_BLOCK

    if lines[0].startswith("- "):
        for i in range(1, len(lines)):
            if not lines[i].startswith("- "):
                break
            if i == len(lines)-1:
                return BlockType.UNORDERED_LIST_BLOCK

    if lines[0].startswith("1. "):
        for i in range(1, len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                break
            if i == len(lines)-1:
                return BlockType.ORDERED_LIST_BLOCK

    return BlockType.PARAGRAPH_BLOCK