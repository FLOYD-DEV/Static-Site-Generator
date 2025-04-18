from textnode import TextNode, TextType

def main():
    # Print "hello world" to satisfy initial requirement
    print("hello world")
    # Create a TextNode with dummy values
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # Print the node to verify __repr__
    print(node)

if __name__ == "__main__":
    main()