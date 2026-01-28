class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")

    def props_to_html(self):
        if not self.props:
            return ""
        html = "".join(f' {key}="{value}"' for key, value in self.props.items())
        return html