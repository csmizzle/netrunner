from networkx import Graph
from networkx.classes.reportviews import DegreeView
from netrunner.models import NodeMap, EdgeMap
from typing import List, Tuple, Iterable
import pandas as pd
from pandas.core.frame import DataFrame


class NetFrame:

    def __init__(self, dataframe: DataFrame, nodes: List[str] = None,
                 links: List[tuple] = None, ignore_chars: str = None):

        # TODO: add edge map updates
        # TODO: update json output based on attributes
        # TODO: edge attributes

        self.frame = dataframe.fillna('None')
        self.net = Graph()
        self.node_map = NodeMap()
        self.edge_map = EdgeMap()

        # parse optional input params and create network if both present
        if nodes:
            self.add_nodes(cols=nodes, ignore_chars=ignore_chars)

        if links:
            self.add_edges(cols=links, ignore_chars=ignore_chars)

        if nodes and links:
            self.populate_network()

    @staticmethod
    def get_values(dataframe, col_name: str, ignore_chars: str) -> list:

        if ignore_chars:
            nodes = list(set([node for node in list(dataframe[col_name]) if str(node) != ignore_chars]))

        else:
            nodes = list(set([node for node in list(dataframe[col_name])]))

        return nodes

    def create_nodes(self, cols: list, ignore_chars: str) -> list:
        """
        Iterate and creat all nodes given column names

        :param cols: list
        :param ignore_chars: str
        :return: list
        """

        all_nodes = list()

        for col in cols:

            nodes = self.get_values(self.frame, col, ignore_chars)

            all_nodes.extend(nodes)

        return all_nodes

    @staticmethod
    def get_edges(dataframe: DataFrame, target_col: str, source_col: str, ignore_str: str = None) -> list:
        """
        Get relationships

        :param dataframe: DataFrame
        :param target_col: str
        :param source_col: str
        :param ignore_str: str
        :return: list
        """

        if ignore_str:
            return list(zip(
                list(dataframe[dataframe[source_col] != ignore_str][source_col]),
                list(dataframe[dataframe[target_col] != ignore_str][target_col])
            ))

        return list(zip(
            list(dataframe[source_col]),
            list(dataframe[target_col])
        ))

    def add_nodes(self, cols: list, ignore_chars: str = None) -> None:
        """
        format nodes for visualization

        :param cols: list
        :param ignore_chars: str

        """

        # TODO: add groups

        nodes = self.create_nodes(cols, ignore_chars)

        if len(nodes) > 0:

            # set nodes in map
            self.node_map.update(nodes)

    def create_edges(self, cols: List[Tuple], ignore_chars: str = None) -> list:
        """
        format edges

        :param cols:
        :param ignore_chars:
        :return:
        """

        all_edges = list()

        for col in cols:
            edges = self.get_edges(self.frame, col[0], col[1], ignore_chars)
            all_edges.extend(edges)

        return all_edges

    def add_edges(self, cols: List[Tuple], ignore_chars: str = None) -> None:
        """
        Store edges for visualization

        :param cols:
        :param ignore_chars:
        """

        edges = self.create_edges(cols, ignore_chars)

        if len(edges) > 0:
            self.edge_map.update(edges)

    def to_json(self) -> dict:
        """
        merge links and edges

        :return: dict
        """

        nodes = dict()
        format_nodes = list()
        edges = dict()
        links = list()

        for node in self.node_map.map.keys():
            entry = dict(id=node, group=1)
            format_nodes.append(entry)

        nodes.update({
            'nodes': format_nodes
        })

        for edge in self.edge_map.map.keys():
            entry = dict(source=edge[0], target=edge[1], value=1)
            links.append(entry)

        edges.update({
            'links': links
        })

        return {**nodes, **edges}

    def populate_network(self) -> None:
        """
        Create NetworkX Graph from Node and Edge Maps

        :return:
        """

        nodes = [node for node in self.node_map.map.keys()]
        edges = [(edge[0], edge[1]) for edge in self.edge_map.map.keys()]
        self.net.add_nodes_from(nodes)
        self.net.add_edges_from(edges)

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

    def join_graph(self, netframe) -> None:
        """
        Join two NetFrames together into current NetFrame

        :param netframe: NetFrame to join on

        """

        # join graphs and flush stats based on old net
        nodes = set(list(netframe.node_map.map.keys()) + list(self.node_map.map.keys()))
        edges = list(netframe.edge_map.map.keys()) + list(self.edge_map.map.keys())

        # flush and update
        self.node_map.flush()
        self.node_map.update(nodes)
        self.edge_map.flush()
        self.edge_map.update(edges)

        # repopulate network
        self.populate_network()

    def join_all(self, netframe, left_on: str, right_on: str,  how: str = 'left') -> None:
        """
        Join both graph and dataframe together on single column

        :param netframe: NetFrame
        :param left_on: str
        :param right_on: str
        :param how: str
        """

        self.frame = pd.merge(left=self.frame, right=netframe.frame,
                              left_on=left_on, right_on=right_on, how=how)
        self.join_graph(netframe)
