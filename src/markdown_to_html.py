from htmlnode import LeafNode, ParentNode
from textnode import TextType, text_to_textnodes
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    lines = block.split('\n')

    if block_type == BlockType.HEADING:
        level = 1
        while lines[0].startswith("#"):
            lines[0] = lines[0][1:]
            level += 1
        tag = f"h{min(6, level)}"
        return ParentNode(tag, [LeafNode(None, lines[0].strip())])
    elif block_type == BlockType.CODE:
        content = "\n".join(lines[1:-1])
        return ParentNode("pre", [LeafNode("code", content)])
    elif block_type == BlockType.QUOTE:
        children = [LeafNode(None, line[1:].strip()) for line in lines]
        return ParentNode("blockquote", children)
    elif block_type == BlockType.ULIST:
        items = [ParentNode("li", [LeafNode(None, line[2:].strip())]) for line in lines]
        return ParentNode("ul", items)
    elif block_type == BlockType.OLIST:
        items = []
        for line in lines:
            number = line.split(".")[0].strip()
            content = ".".join(line.split(".")[1:]).strip()
            items.append(ParentNode("li", [LeafNode(None, content)]))
        return ParentNode("ol", items)
    elif block_type == BlockType.PARAGRAPH:
        nodes = text_to_textnodes(block)
        children = []
        for node in nodes:
            if node.text_type == TextType.LINK:
                children.append(LeafNode("a", node.text, {"href": node.url}))
            elif node.text_type == TextType.IMAGE:
                children.append(LeafNode("img", "", {"src": node.url, "alt": node.text}))
            elif node.text_type == TextType.BOLD:
                children.append(LeafNode("b", node.text))
            elif node.text_type == TextType.ITALIC:
                children.append(LeafNode("i", node.text))
            elif node.text_type == TextType.CODE:
                children.append(LeafNode("code", node.text))
            else:
                children.append(LeafNode(None, node.text))
        return ParentNode("p", children)
    return LeafNode(None, block) # Fallback

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = [block_to_html_node(block) for block in blocks]
    return ParentNode(None, html_nodes) # Root node