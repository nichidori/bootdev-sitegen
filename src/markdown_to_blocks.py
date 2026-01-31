def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        b = block.strip()
        if b:
            final_blocks.append(b)
    return final_blocks
    