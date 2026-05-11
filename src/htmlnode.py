class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_htlm(self):
        final = ""
        if not self.props:
            return ""
        for key in self.props:
            
            final += f' {key}="{self.props[key]}"'
        return final
    
    def __repr__(self):
        return f"HTMLNODE: tag={self.tag} value={self.value} children={self.children} props={self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        match self.tag:
            case "p":
                return f"<p>{self.value}</p>"
            case "a":
                return f'<a{self.props_to_htlm()}>{self.value}</a>'
            case "span":
                return f"<span>{self.value}</span>"
            case "b":
                return f"<b>{self.value}</b>"
            case "i":
                return f"<i>{self.value}</i>"
            case "li":
                return f"<li>{self.value}</li>"
            case "pre":
                return f"<pre>{self.value}</pre>"
            case _:
                return f"{self.value}"
    def __repr__(self):
        return f"LEAF: tag={self.tag} value={self.value} props={self.props}"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("no children")
        final = f"<{self.tag}>"
        for child in self.children:
            final += child.to_html()
        return final + f"</{self.tag}>"
    
