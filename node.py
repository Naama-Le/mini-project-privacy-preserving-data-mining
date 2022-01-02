class Node:
    """Contains the information of the node and another nodes of the Decision Tree."""

    def __init__(self, attrs, value):
        self.attrs = attrs
        self.value = value
        self.next = None
        self.children = None
