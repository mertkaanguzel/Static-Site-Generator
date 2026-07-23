
from leafnode import LeafNode
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Invalid HTML: no tag")
        
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        
        html_string = f'<{self.tag}{self.props_to_html()}>'

        for node in self.children:
            html_string += node.to_html()
            
        html_string += f'</{self.tag}>'
        return html_string
    
    def __repr__(self) -> str:
        return f"""
        HTMLNode(tag: {self.tag} ,
        children: {self.children} , 
        props: {self.props}
        """
