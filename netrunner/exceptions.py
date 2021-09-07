"""
Netrunner exceptions

"""


class EmptyEdgeLabelException(BaseException):
    def __init__(self, edge: tuple) -> None:
        self.edge = edge

    def __str__(self) -> str:
        return f"{self.edge}'s label has not been set"
