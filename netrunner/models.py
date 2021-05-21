"""
Custom models for NetFrames

"""
from collections import namedtuple
from typing import Iterable


# Node object
Node = namedtuple('Node', ['name', 'attributes', 'source_col'])

# Edge object
Edge = namedtuple('Edge', ['name', 'attributes', 'source_col', 'target_col'])

# Utility Models
DrawResults = namedtuple('DrawResults', ['nodes', 'links'])


# NetFrame Models
class NodeMap:

    def __init__(self) -> None:
        self.map = dict()

    @staticmethod
    def update_node_map(node: Node, node_map: dict):
        """
        Logic for indexing new nodes into a node map

        :param node:
        :param node_map:
        :return:
        """

        if node.name not in node_map.keys():

            # check if attributes are present
            if node.attributes:
                # add node if not present in current map
                node_map.update({
                    node.name: {
                        'attributes': node.attributes,
                        'source_col': [node.source_col]
                    }
                })

            # if attributes are net present, we want an empty dict to hold place ready for data
            else:
                node_map.update({
                    node.name: {
                        'attributes': dict(),
                        'source_col': [node.source_col]
                    }
                })

        # if node present, check if the source matches current node
        elif node.name in node_map.keys():

            if node.source_col not in node_map[node.name]['source_col']:
                node_map[node.name]['source_col'].append(node.source_col)

            else:
                print(f'Node {node.name} already created!')

    def update(self, nodes: Iterable[Node]) -> None:
        """
        Create NodeMap

        :return:
        """

        for node in nodes:
            self.update_node_map(node, self.map)

    def flush(self) -> None:
        """
        clear mapping

        """

        self.map = dict()


class EdgeMap:

    def __init__(self) -> None:

        # TODO: Allow for multiple edges with same source/target mapping
        # - this can be done with lists under the source/target key
        self.map = dict()

    @staticmethod
    def update_edge_map(edge, edge_map: dict) -> None:
        """
        Create NodeMap

        :return:
        """

        if edge.name not in edge_map.keys():
            # check if edge attributes are present
            if edge.attributes:

                edge_map.update({
                    edge.name : {
                        'attributes': edge.attributes,
                        'source_col': edge.source_col,
                        'target_col': edge.target_col
                    }
                })

            else:
                edge_map.update({
                    edge.name : {
                        'attributes': dict(),
                        'source_col': edge.source_col,
                        'target_col': edge.target_col
                    }
                })

    def update(self, edges: Iterable[Edge]):
        """

        :return:
        """

        for edge in edges:
            self.update_edge_map(edge, self.map)

    def flush(self) -> None:
        """
        clear mapping

        """

        self.map = dict()
