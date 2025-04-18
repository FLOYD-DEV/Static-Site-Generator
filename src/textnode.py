from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

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
import re

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