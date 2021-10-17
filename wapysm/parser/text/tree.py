from typing import List, Union


class SComponent():
    """ Base class for S-expression components """
    pass

class SValue(SComponent):
    """ Constant value of S-expression """
    value: Union[int, float, str]

    def __init__(self, value: Union[int, float, str]) -> None:
        super().__init__()
        self.value = value

    def __eq__(self, o: object) -> bool:
        return isinstance(o, SValue) and o.value == self.value

class SLabel(SComponent):
    """ Label of S-expression """
    value: str

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __eq__(self, o: object) -> bool:
        return isinstance(o, SLabel) and o.value == self.value

class SNode(SComponent):
    """
    Node of S-expression.
    A node can contain any nodes, label and values.
    """
    label: str
    children: List[SComponent]

    def __init__(self, label: str, children: List[SComponent] = None) -> None:
        super().__init__()
        self.label = label
        self.children = children or []
