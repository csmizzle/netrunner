"""
Custom models for NetFrames

"""
from collections import namedtuple
from typing import Iterable


# Node object
Node = namedtuple('Node', ['name', 'attributes', 'source_col'])


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

    def update(self, edges) -> None:
        """
        Create NodeMap

        :return:
        """

        self.map = {
            (edge[0], edge[1]): {  # unpack source / target into map tuple
                'attributes': {},
                'source_col': edge[2],  # source column for updating and deleting
                'target_col': edge[3]  # target column for updating and deleting
            }
            for edge in edges
        }

    def flush(self) -> None:
        """
        clear mapping

        """

        self.map = dict()


# Utility Models
DrawResults = namedtuple('DrawResults', ['nodes', 'links'])
