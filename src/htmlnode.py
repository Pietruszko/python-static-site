class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self):
        if not self.props:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.tag == "img":
            if not self.props or "src" not in self.props:
                raise ValueError("img tag requires src attribute")
            alt = self.props.get("alt", "")
            return f'<img src="{self.props["src"]}" alt="{alt}" />'
        
        if not self.value:
            raise ValueError
        
        if not self.tag:
            return self.value
        
        props_html = ""
        if self.props:
            for key, value in self.props.items():
                props_html += f' {key}="{value}"'
        
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError
        html = []
        for child in self.children:
            html.append(child.to_html())
        return "<" + self.tag + ">" + "".join(html) + "</" + self.tag + ">"


