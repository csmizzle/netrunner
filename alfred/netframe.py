from networkx import Graph
from networkx.classes.reportviews import DegreeView
from .models import NodeMap, EdgeMap
from typing import List, Tuple, Iterable, Dict
from pandas.core.frame import DataFrame


class NetFrame:

    def __init__(self, dataframe: DataFrame):

        # TODO: add edge map updates
        # TODO: update json output based on attributes

        self.dataframe = dataframe
        self.graph = Graph()
        self.node_map = NodeMap()
        self.edge_map = EdgeMap()

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
        :return:
        """

        all_nodes = list()

        for col in cols:

            nodes = self.get_values(self.dataframe, col, ignore_chars)

            all_nodes.extend(nodes)

        return all_nodes

    @staticmethod
    def get_edges(dataframe: DataFrame, target_col: str, source_col: str, ignore_str: str = None) -> list:
        """
        Get relationships

        :param dataframe:
        :param target_col:
        :param source_col:
        :param ignore_str:
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

    def format_nodes(self, cols: list, ignore_chars: str = None) -> None:
        """
        format nodes for visualization

        :param cols: list
        :param ignore_chars: str

        """

        # TODO: add groups

        format_nodes = list()
        nodes = self.create_nodes(cols, ignore_chars)

        if len(nodes) > 0:

            # set nodes in map
            self.node_map.set_map(nodes)

    def create_edges(self, cols: List[Tuple], ignore_chars: str = None) -> list:
        """
        format edges

        :param cols:
        :param ignore_chars:
        :return:
        """

        all_edges = list()

        for col in cols:
            edges = self.get_edges(self.dataframe, col[0], col[1], ignore_chars)
            all_edges.extend(edges)

        return all_edges

    def format_edges(self, cols: List[Tuple], ignore_chars: str = None) -> None:
        """
        Store edges for visualization

        :param cols:
        :param ignore_chars:
        """

        links = list()
        edges = self.create_edges(cols, ignore_chars)

        if len(edges) > 0:

            self.edge_map.set_map(edges)

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
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)

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


