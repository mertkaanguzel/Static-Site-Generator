from textnode import TextNode, TextType
import re

def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes: list[TextNode] = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown Syntax: formatted section not closed")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.PLAIN_TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?\..*?)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"\[(.*?)\]\((.*?\..*?)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE_TEXT,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK_TEXT, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))
    return new_nodes

def split_nodes_image_alternative(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes: list[TextNode] = []
        sections = re.split(r"!\[(.*?)\]\((.*?\..*?)\)", old_node.text)
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue

            if i % 3 == 0:
                split_nodes.append(TextNode(sections[i], TextType.PLAIN_TEXT))
            elif i % 3 == 1:
                continue
            elif i % 3 == 2:
                split_nodes.append(TextNode(sections[i-1], TextType.IMAGE_TEXT, sections[i]))

        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_link_alternative(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
        
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes: list[TextNode] = []
        sections = re.split(r"\[(.*?)\]\((.*?\..*?)\)", old_node.text)
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue

            if i % 3 == 0:
                split_nodes.append(TextNode(sections[i], TextType.PLAIN_TEXT))
            elif i % 3 == 1:
                continue
            elif i % 3 == 2:
                split_nodes.append(TextNode(sections[i-1], TextType.LINK_TEXT, sections[i]))

        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_delimiter_alternative(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    delimiter_len = len(delimiter)-1
    delimiter = r"\*\*" if delimiter == "**" else delimiter

    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        indices = [match.start() for match in re.finditer(delimiter, old_node.text)]

        if len(indices) == 0:
            new_nodes.append(old_node)
            continue

        if len(indices) % 2 != 0:
            raise ValueError("Invalid Markdown Syntax: formatted section not closed")

        for i in range(0, len(indices), 2):
            prev_index = indices[i-1]+1+delimiter_len if i > 0 else 0
            plain_text = old_node.text[prev_index : indices[i]]

            not_plain_text = old_node.text[indices[i]+1+delimiter_len : indices[i+1]]

            if plain_text:
                new_nodes.append(TextNode(plain_text, TextType.PLAIN_TEXT))

            if not_plain_text:
                new_nodes.append(TextNode(not_plain_text, text_type))

        if indices[len(indices)-1]+delimiter_len < len(old_node.text)-1:
            last_plain_text = old_node.text[indices[len(indices)-1]+1+delimiter_len:]
            new_nodes.append(TextNode(last_plain_text, TextType.PLAIN_TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    textnodes = split_nodes_delimiter([TextNode(text, TextType.PLAIN_TEXT)], "**", TextType.BOLD_TEXT)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC_TEXT)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE_TEXT)
    textnodes = split_nodes_image(textnodes)
    return split_nodes_link(textnodes)