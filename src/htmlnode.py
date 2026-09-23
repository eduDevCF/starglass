

class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        formatted = ""
        if self.props:
            for key, value in self.props:
                formatted += f' {key}="{value}"'
        return formatted

    def __repr__(self):
        return f"{self.tag}  PROPS: {self.props}  VALUE: {self.value}  CHILDREN: {self.children}"
