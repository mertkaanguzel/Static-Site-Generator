from textnode import TextNode, TextType

def main() -> None:
    textnode = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(textnode)

main()
