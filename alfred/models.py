"""
Custom models for NetFrames

"""


class NodeMap:

    def __init__(self):
        self.map = dict()

    def set_map(self, nodes) -> None:
        """
        Create NodeMap

        :return:
        """

        self.map = {node: {'attributes': {}} for node in nodes}


class EdgeMap:

    def __init__(self):
        self.map = dict()

    def set_map(self, edges) -> None:
        """
        Create NodeMap

        :return:
        """

        self.map = {edge: {'attributes': {}} for edge in edges}
