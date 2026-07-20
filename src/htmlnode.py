class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        if value is None and children is None:
            raise ValueError("Value and Children Can't Be Null At The Same Time")
        
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()
    
    def __repr__(self) -> str:
        return f"""
        HTMLNode(tag: {self.tag}, value: {self.value} ,
        children: {self.children} , 
        props: {self.props}
        """

    def to_html(self) -> None:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        
        props_string = ""
        
        for key, value in self.props.items():
            props_string += f'{key}="{value}" '
        return props_string[:-1]