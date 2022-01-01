class Node:
    """Contains the information of the node and another nodes of the Decision Tree."""

    def __init__(self, attrs, test):
        self.attrs = attrs
        self.test = test
        self.next = None
        self.children = None
