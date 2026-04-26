from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    cleaned_blocks = []

    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            cleaned_blocks.append(stripped)

    return cleaned_blocks

from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith("#"):
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and block[count] == " ":
            return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST

    is_ordered = True
    expected = 1
    for line in lines:
        if not line.startswith(f"{expected}. "):
            is_ordered = False
            break
        expected += 1
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            children.append(ParentNode("p", text_to_children(text)))

        elif block_type == BlockType.HEADING:
            heading_level = 0
            for char in block:
                if char == "#":
                    heading_level += 1
                else:
                    break

            text = block[heading_level + 1:]
            children.append(ParentNode(f"h{heading_level}", text_to_children(text)))

        elif block_type == BlockType.CODE:
            text = block[4:-3]
            code_node = text_node_to_html_node(TextNode(text, TextType.CODE))
            children.append(ParentNode("pre", [code_node]))

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned_lines = []

            for line in lines:
                cleaned_lines.append(line.lstrip(">").strip())

            text = " ".join(cleaned_lines)
            children.append(ParentNode("blockquote", text_to_children(text)))

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            list_items = []

            for line in lines:
                text = line[2:]
                list_items.append(ParentNode("li", text_to_children(text)))

            children.append(ParentNode("ul", list_items))

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            list_items = []

            for line in lines:
                text = line.split(". ", 1)[1]
                list_items.append(ParentNode("li", text_to_children(text)))

            children.append(ParentNode("ol", list_items))

    return ParentNode("div", children)
