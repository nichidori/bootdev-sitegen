from block_type import BlockType
from block_to_block_type import block_to_block_type
from leafnode import LeafNode
from markdown_to_blocks import markdown_to_blocks
from parentnode import ParentNode
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType
from textnode_to_htmlnode import text_node_to_html_node


def markdown_to_html_node(markdown):
    if not markdown.strip():
        return LeafNode("div", "")
        
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        node = None

        match block_type:
            case BlockType.PARAGRAPH:
                text = block.replace("\n", " ")
                children = text_to_children(text)
                node = ParentNode("p", children)

            case BlockType.HEADING:
                sections = block.split(" ", 1)
                level = len(sections[0])
                text = sections[1]
                children = text_to_children(text)
                node = ParentNode(f"h{level}", children)

            case BlockType.CODE:
                text = block.replace("```", "").lstrip()
                text_node = TextNode(text, TextType.CODE)
                children = [text_node_to_html_node(text_node)]
                node = ParentNode("pre", children)

            case BlockType.QUOTE:
                lines = block.split("\n")
                text = " ".join(line.replace(">", "", 1).strip() for line in lines)
                children = text_to_children(text)
                node = ParentNode("blockquote", children)

            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_children = []
                for line in lines:
                    text = line.replace("- ", "", 1).strip()
                    children = text_to_children(text)
                    li_node = ParentNode("li", children)
                    list_children.append(li_node)
                node = ParentNode("ul", list_children)

            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                list_children = []
                for i, line in enumerate(lines):
                    text = line.replace(f"{i+1}. ", "", 1).strip()
                    children = text_to_children(text)
                    li_node = ParentNode("li", children)
                    list_children.append(li_node)
                node = ParentNode("ol", list_children)

        block_nodes.append(node)

    return ParentNode("div", block_nodes)


def text_to_children(text):
    html_nodes = []
    for node in text_to_textnodes(text):
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes
