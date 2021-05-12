"""
Custom models for NetFrames

"""
from collections import namedtuple
from typing import Iterable


# NetFrame Models
class NodeMap:

    def __init__(self) -> None:
        self.map = dict()

    @staticmethod
    def update_node_map(node: tuple, node_map: dict):
        """
        Logic for indexing new nodes into a node map

        :param node:
        :param node_map:
        :return:
        """

        if node[0] not in node_map.keys():

            # add node if not present in current map
            node_map.update({
                node[0]: {
                    'attributes': {},
                    'source_col': [node[1]]
                }
            })

        # if node present, check if the source matches current node
        elif node[0] in node_map.keys():

            if node[1] not in node_map[node[0]]['source_col']:
                node_map[node[0]]['source_col'].append(node[1])

            else:
                print(f'Node {node} already created!')

    def update(self, nodes: Iterable) -> None:
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
