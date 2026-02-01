import re

from block_type import BlockType


def block_to_block_type(block):
    lines = block.split("\n")

    if lines and re.match(r"^#{1,6}\s", lines[0]):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if lines and all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if lines:
        expected = 1
        for line in lines:
            if not line.startswith(f"{expected}. "):
                break
            expected += 1
        else:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
