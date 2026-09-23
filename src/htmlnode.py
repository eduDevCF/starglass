

class HTMLNode():
    def __init__(
        self, 
        tag: str | None = None, 
        value: str | None = None, 
        children: list["HTMLNode"] | None = None, 
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        formatted = ""
        if self.props:
            for key, value in self.props.items():
                formatted += f' {key}="{value}"'
        return formatted

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}  CHILDREN: {self.children}  PROPS: {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str]= None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value and self.tag != "img":
            raise ValueError("required value is missing")
        if not self.tag:
            return self.value
        html = f"<{self.tag}"
        if self.props:
            html += self.props_to_html()
        html += ">"
        if self.tag != "img":
            html += f"{self.value}</{self.tag}>"
        return html

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}  PROPS: {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("tag cannot be empty for ParentNodes")
        if not self.children:
            raise ValueError("missing children from ParentNode")
        html = f"<{self.tag}{self.props_to_html()}>"
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        if child_html:
            html += child_html
        html += f"</{self.tag}>"
        return html
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

