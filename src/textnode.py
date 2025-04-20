from enum import Enum
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        for i, part in enumerate(parts):
            if part:
                node_type = text_type if i % 2 == 1 else TextType.TEXT
                new_nodes.append(TextNode(part, node_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r'(?<!\!)\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        matches = re.finditer(r'!\[(.*?)\]\((.*?)\)', text)
        last_end = 0
        temp_nodes = []
        for match in matches:
            start, end = match.span()
            alt_text, url = match.groups()
            if last_end < start:
                temp_nodes.append(TextNode(text[last_end:start], TextType.TEXT))
            temp_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_end = end
        if last_end < len(text):
            temp_nodes.append(TextNode(text[last_end:], TextType.TEXT))
        if not temp_nodes:
            new_nodes.append(node)
        else:
            new_nodes.extend(temp_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        matches = re.finditer(r'(?<!\!)\[(.*?)\]\((.*?)\)', text)
        last_end = 0
        temp_nodes = []
        for match in matches:
            start, end = match.span()
            link_text, url = match.groups()
            if last_end < start:
                temp_nodes.append(TextNode(text[last_end:start], TextType.TEXT))
            temp_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_end = end
        if last_end < len(text):
            temp_nodes.append(TextNode(text[last_end:], TextType.TEXT))
        if not temp_nodes:
            new_nodes.append(node)
        else:
            new_nodes.extend(temp_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = [block.strip() for block in blocks if block.strip()]
    return cleaned_blocks

def block_to_block_type(block):
    # Heading: Starts with 1-6 # followed by a space
    if re.match(r'^#{1,6}\s', block):
        return BlockType.HEADING
    # Code: Starts with ``` and ends with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    # Quote: Every line starts with >
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines if line):
        return BlockType.QUOTE
    # Unordered list: Every line starts with - followed by a space
    if all(line.startswith("- ") for line in lines if line):
        return BlockType.UNORDERED_LIST
    # Ordered list: Lines start with number. (e.g., 1., 2.), starting at 1 and incrementing
    if lines and re.match(r'^1\.\s', lines[0]):
        for i, line in enumerate(lines, 1):
            if line and not re.match(f'^{i}\\.\\s', line):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    # Default: Paragraph
    return BlockType.PARAGRAPH