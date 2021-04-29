from .utils import unpack_source_col
from networkx import Graph
from networkx.readwrite import json_graph
from networkx.classes.reportviews import DegreeView
from netrunner.models import NodeMap, EdgeMap
from typing import List, Tuple, Iterable
import pandas as pd
from pandas.core.frame import DataFrame


class NetFrame:

    def __init__(self, dataframe: DataFrame, nodes: List[str] = None,
                 links: List[tuple] = None, ignore_chars: str = None):

        # TODO: Delete nodes and edges
        # TODO: if dataframe changes, give ability to propagate changes to network

        self.frame = dataframe.fillna('None')
        self.net = Graph()
        self.node_map = NodeMap()
        self.edge_map = EdgeMap()
        self.node_columns = list()
        self.edge_columns = list()

        # parse optional input params and create network if both present
        if nodes:
            self.add_nodes(cols=nodes, ignore_chars=ignore_chars)

        if links:
            self.add_edges(cols=links, ignore_chars=ignore_chars)

        if nodes and links:
            self.populate_network()

    # Node/Edge Operations
    @staticmethod
    def _get_nodes(dataframe, col_name: str, ignore_chars: str) -> List[Tuple]:

        if ignore_chars:
            nodes = list(set([(node, col_name) for node in list(dataframe[col_name]) if str(node) != ignore_chars]))

        else:
            nodes = list(set([(node, col_name) for node in list(dataframe[col_name])]))

        return nodes

    def _create_nodes(self, cols: list, ignore_chars: str) -> list:
        """
        Iterate and creat all nodes given column names

        :param cols: list
        :param ignore_chars: str
        :return: list
        """

        all_nodes = list()

        for col in cols:
            nodes = self._get_nodes(self.frame, col, ignore_chars)

            # update node cols and create list of nodes for network
            all_nodes.extend(nodes)

            if col not in self.node_columns:
                self.node_columns.append(col)

        return all_nodes

    @staticmethod
    def _get_edges(dataframe: DataFrame, target_col: str, source_col: str, ignore_str: str = None) -> list:
        """
        Get relationships

        :param dataframe: DataFrame
        :param target_col: str
        :param source_col: str
        :param ignore_str: str
        :return: list
        """

        if ignore_str:

            source_data = dataframe[dataframe[source_col] != ignore_str][source_col]
            target_data = dataframe[dataframe[target_col] != ignore_str][target_col]

            return list(zip(
                list(source_data),
                list(target_data),
                list(source_col)*len(source_data),
                list(target_col)*len(target_data)
            ))

        return list(zip(
            list(dataframe[source_col]),
            list(dataframe[target_col]),
            [source_col] * len(dataframe[source_col]),
            [target_col] * len(dataframe[target_col])
        ))

    def add_nodes(self, cols: list, ignore_chars: str = None) -> None:
        """
        format nodes for visualization

        :param cols: list
        :param ignore_chars: str

        """

        nodes = self._create_nodes(cols, ignore_chars)

        if len(nodes) > 0:

            # set nodes in map
            self.node_map.update(nodes)

    def _create_edges(self, cols: List[Tuple], ignore_chars: str = None) -> list:
        """
        format edges

        :param cols:
        :param ignore_chars:
        :return:
        """

        all_edges = list()

        for col in cols:
            edges = self._get_edges(self.frame, col[0], col[1], ignore_chars)

            # update edges map and edges for network
            all_edges.extend(edges)

            if col not in self.edge_columns:
                self.edge_columns.append(col)

        return all_edges

    def add_edges(self, cols: List[Tuple], ignore_chars: str = None) -> None:
        """
        Store edges for visualization

        :param cols:
        :param ignore_chars:
        """

        edges = self._create_edges(cols, ignore_chars)

        if len(edges) > 0:
            self.edge_map.update(edges)

    def delete_node(self, node: str) -> None:
        """
        Delete node by name in Net

        :param node: str
            node label
        """

        pass

    # Network Operations
    def populate_network(self) -> None:
        """
        Create NetworkX Graph from Node and Edge Maps

        :return:
        """

        nodes = [node for node in self.node_map.map.keys()]
        edges = [(edge[0], edge[1]) for edge in self.edge_map.map.keys()]
        self.net.add_nodes_from(nodes)
        self.net.add_edges_from(edges)

    def flush_network(self) -> None:
        """
        Flush network empty
:
        """

        self.net = Graph()

    def update_node_map(self, values: Iterable, type_: str) -> None:
        """
        set new values for nodes

        :param values: Iterable
        :param type_: str
        """

        if isinstance(values, DegreeView):

            for value in values:

                self.node_map.map[value[0]]['attributes'].update({
                    type_: value[1]
                })

        if isinstance(values, dict):

            for key, value in values.items():
                self.node_map.map[key]['attributes'].update({
                    type_: value
                })

        if isinstance(values, list):

            # communities come back in frozen sets in networkX
            for idx, value in enumerate(values):

                if isinstance(value, frozenset):

                    for entity in value:

                        self.node_map.map[entity]['attributes'].update({
                            type_: idx
                        })

    def to_json(self) -> dict:
        """
        Test networkx json implementation

        :return: dict
        """

        return json_graph.node_link_data(self.net)

    def join_graph(self, netframe) -> None:
        """
        Join two NetFrames together into current NetFrame

        :param netframe: NetFrame to join on

        """

        # list of nodes to pass to graph
        nodes = list()

        for node in netframe.node_map.map.keys():
            nodes.extend(unpack_source_col(node, netframe.node_map.map))

        for node in self.node_map.map.keys():
            nodes.extend(unpack_source_col(node, self.node_map.map))

        nodes = set(nodes)

        # list of edges to pass to new graph
        edges = list()

        for edge in netframe.edge_map.map.keys():
            edges.append((edge[0], edge[1],
                          netframe.edge_map.map[(edge[0], edge[1])]['source_col'],
                          netframe.edge_map.map[(edge[0], edge[1])]['target_col']))

        for edge in self.edge_map.map.keys():
            edges.append((edge[0], edge[1],
                          self.edge_map.map[(edge[0], edge[1])]['source_col'],
                          self.edge_map.map[(edge[0], edge[1])]['target_col']))

        # flush and update nodes and edges
        self.node_map.flush()
        self.node_map.update(nodes)
        self.edge_map.flush()
        self.edge_map.update(edges)

        # join meta data mappings
        self.node_columns.extend(netframe.node_columns)
        self.edge_columns.extend(netframe.edge_columns)

        # repopulate network
        self.populate_network()

    def join_all(self, netframe, left_on: str, right_on: str,  how: str = 'left') -> None:
        """
        Join both graph and dataframe together on single column, left join outward from NetFrame

        :param netframe: NetFrame
        :param left_on: str
        :param right_on: str
        :param how: str
        """

        # TODO: revisit this

        self.frame = pd.merge(left=self.frame, right=netframe.frame, left_on=left_on, right_on=right_on, how=how)
        self.join_graph(netframe)

    def apply_dataframe(self) -> None:
        """
        Apply frame changes to net

        """

        # flush maps and network
        self.node_map.flush()
        self.edge_map.flush()
        self.flush_network()

        # apply new changes from frame to net
        self.add_nodes(self.node_columns)
        self.add_edges(self.edge_columns)
        self.populate_network()
