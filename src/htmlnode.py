

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string = ""
        if self.props is not None:
            for p in self.props:
                prop_string += f" {p}=\"{self.props[p]}\""
        return prop_string

    def __eq__(self, o):
        return self.tag == o.tag and self.value == o.value and \
            self.children == o.children and self.props == o.props

    def __repr__(self):
        return f"<{self.tag} p:{self.props}> v:{self.value} c:{self.children}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("missing tag")
        if self.children is None:
            raise ValueError("missing children for parent")

        returner = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            returner += child.to_html()
        returner += f"</{self.tag}>"
        return returner
