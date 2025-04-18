import unittest
from textnode import TextNode, TextType, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        node = TextNode("Text with **bold** part", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" part", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic(self):
        node = TextNode("Text with _italic_ part", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" part", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], matches)

    def test_extract_no_images(self):
        text = "This is plain text [link](https://www.boot.dev)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        text = "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)

    def test_extract_no_links(self):
        text = "This is plain text ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_mixed_content(self):
        text = "![img](https://i.imgur.com/aKaOqIh.gif) and [link](https://www.boot.dev)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("img", "https://i.imgur.com/aKaOqIh.gif")], image_matches)
        self.assertListEqual([("link", "https://www.boot.dev")], link_matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode("An ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("An ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is plain text [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_non_text_node(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode("A [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("This is plain text ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_non_text_node(self):
        node = TextNode("Italic text", TextType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_mixed_image_and_link(self):
        node = TextNode(
            "Text with ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and [link](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_simple(self):
        text = "Plain **bold** text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Plain ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_no_markdown(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is plain text", TextType.TEXT)],
            nodes,
        )

    def test_text_to_textnodes_image_only(self):
        text = "![image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            nodes,
        )

    def test_text_to_textnodes_mixed(self):
        text = "**Bold** and _italic_ with [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()