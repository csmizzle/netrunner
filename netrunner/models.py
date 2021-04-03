"""
Custom models for NetFrames

"""
import numpy as np


class NodeMap:

    def __init__(self):
        self.map = dict()

    def update(self, nodes) -> None:
        """
        Create NodeMap

        :return:
        """

        self.map = {node: {'attributes': {}}
                    for node in nodes if node not in self.map.keys()}

    def flush(self) -> None:
        """
        clear mapping

        """

        self.map = dict()


class EdgeMap:

    def __init__(self):

        # TODO: Allow for multiple edges with same source/target mapping
        # - this can be done with lists under the source/target key
        self.map = dict()

    def update(self, edges) -> None:
        """
        Create NodeMap

        :return:
        """

        self.map = {edge: {'attributes': {}} for edge in edges}

    def flush(self) -> None:
        """
        clear mapping

        """

        self.map = dict()
