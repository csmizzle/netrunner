from netrunner.utils import unpack_source_col
from networkx import Graph
from networkx.readwrite import json_graph
from networkx.classes.reportviews import DegreeView
from netrunner.models import NodeMap, EdgeMap, Node, Edge
from typing import List, Tuple, Iterable
import pandas as pd
from pandas.core.frame import DataFrame


class NetFrame:
    """
    Easy to use Networkx and Pandas

    """

    def __init__(self, dataframe: DataFrame, nodes: List[str] = None,
                 links: List[tuple] = None, ignore_chars: str = None,
                 node_attributes: dict = None, edge_attributes: dict = None):

        self.frame = dataframe
        self.net = Graph()
        self.node_map = NodeMap()
        self.edge_map = EdgeMap()
        self.node_columns = list()
        self.edge_columns = list()
        self.node_attributes_map = node_attributes
        self.edge_attributes_map = edge_attributes

        # parse optional input params and create network if both present
        if nodes:
            self.add_nodes(cols=nodes, ignore_chars=ignore_chars)

        if links:
            self.add_edges(cols=links, ignore_chars=ignore_chars)

        if node_attributes:
            self.set_node_attributes(node_attributes)

        if edge_attributes:
            self.set_edge_attributes(edge_attributes)

        if nodes and links:
            self.populate_network()

    # Node Operations
    @staticmethod
    def _get_nodes(dataframe, col_name: str, ignore_chars: str) -> List[Tuple]:

        if ignore_chars:
            nodes = list(set([Node(name=node, attributes=None, source_col=col_name)
                              for node in list(dataframe[col_name])
                              if str(node) != ignore_chars]))

        else:
            nodes = list(set([Node(name=node, attributes=None, source_col=col_name)
                              for node in list(dataframe[col_name])
                              if str(node) != 'nan']))

        return nodes

    def _create_nodes(self, cols: list, ignore_chars: str) -> list:
        """
        Iterate and create all nodes given column names

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

    def add_nodes(self, cols: list, ignore_chars: str = None) -> None:
        """
        update nodes

        :param cols: list
        :param ignore_chars: str

        """

        nodes = self._create_nodes(cols, ignore_chars)

        if len(nodes) > 0:

            # set nodes in map
            self.node_map.update(nodes)

    def _get_node_attributes(self, col: str, attributes: list) -> dict:
        """
        Create attribute mapping for a given node

        :param col:
        :param attributes:
        :return:
        """

        attribute_map = {col: dict()}

        # map each attribute to node value
        # {col_value: {col_name: value, col_name: value, ...}}
        for idx, row in self.frame.iterrows():

            attribute_map[col].update({
                row[col]: {attribute: row[attribute] for attribute in attributes}
            })

        return attribute_map

    def _create_node_attributes(self, node_attributes: dict) -> dict:
        """
        Add specified attributes attributes to nodes

        :param node_attributes:
        :return: dict
        """

        attribute_map = dict()

        for col, attributes in node_attributes.items():

            attribute_map.update(self._get_node_attributes(col, attributes))

        return attribute_map

    def set_node_attributes(self, node_attributes: dict) -> None:
        """
        Set node attributes in NodeMap

        :param node_attributes:
        """

        node_attribute_map = self._create_node_attributes(node_attributes)

        for col in node_attribute_map.keys():

            if col in self.node_columns:

                for node in node_attribute_map[col]:

                    if node in self.node_map.map.keys():

                        self.node_map.map[node]['attributes'].update(node_attribute_map[col][node])

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

    # Edge Operations
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

            return [
                Edge(
                    name=(source, target),
                    attributes=None,
                    source_col=source_col,
                    target_col=target_col
                )
                for source, target in zip(source_data, target_data)
            ]

        return [
            Edge(
                name=(source, target),
                attributes=None,
                source_col=source_col,
                target_col=target_col
            )
            for source, target in zip(dataframe[source_col], dataframe[target_col])
            if str(source) != 'nan' and str(target) != 'nan'
        ]

    def _create_edges(self, cols: List[Tuple], ignore_chars: str = None) -> list:
        """
        format edges

        :param cols:
        :param ignore_chars:
        :return: list
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

    def _get_edge_attributes(self, link, attributes):
        """
        Collect and unpack link and corresponding attributes

        :param link:
        :param attributes:
        :return:
        """

        attribute_map = {link: dict()}

        # map each attribute to edge value
        for idx, row in self.frame.iterrows():

            attribute_map[link].update({

                # reverse tuple since it gets ordered???
                (row[link[1]], row[link[0]]): {attribute: row[attribute] for attribute in attributes}
            })

        return attribute_map

    def _create_edge_attributes(self, edge_attributes: dict) -> dict:
        """
        Add specified attributes attributes to nodes

        :param edge_attributes:
        :return: dict
        """

        attribute_map = dict()

        for link, attributes in edge_attributes.items():
            attribute_map.update(self._get_edge_attributes(link, attributes))

        return attribute_map

    def set_edge_attributes(self, edge_attributes: dict) -> None:
        """
        Set node attributes in NodeMap

        :param edge_attributes:
        """

        edge_attribute_map = self._create_edge_attributes(edge_attributes)

        for col in edge_attribute_map.keys():

            if col in self.edge_columns:

                for edge in edge_attribute_map[col]:

                    if edge in self.edge_map.map.keys():

                        self.edge_map.map[edge]['attributes'].update(edge_attribute_map[col][edge])

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

        nodes = [(node, self.node_map.map[node]['attributes']) for node in self.node_map.map.keys()]
        edges = [(edge[0], edge[1]) for edge in self.edge_map.map.keys()]
        self.net.add_nodes_from(nodes)
        self.net.add_edges_from(edges)

    def flush_network(self) -> None:
        """
        Flush network empty

        """

        self.net = Graph()

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

        # list of edges to pass to new graph
        edges = list()

        for edge in netframe.edge_map.map.keys():
            edges.append(Edge(name=(edge[0], edge[1]),
                              attributes=netframe.edge_map.map[(edge[0], edge[1])]['attributes'],
                              source_col=netframe.edge_map.map[(edge[0], edge[1])]['source_col'],
                              target_col=netframe.edge_map.map[(edge[0], edge[1])]['target_col']))

        for edge in self.edge_map.map.keys():
            edges.append(Edge(name=(edge[0], edge[1]),
                              attributes=self.edge_map.map[(edge[0], edge[1])]['attributes'],
                              source_col=self.edge_map.map[(edge[0], edge[1])]['source_col'],
                              target_col=self.edge_map.map[(edge[0], edge[1])]['target_col']))

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

    def apply_map(self):
        """
        Apply map object stored within in NetFrame

        :return:
        """

        return NetFrame(self.frame,
                        nodes=self.node_columns,
                        links=self.edge_columns,
                        node_attributes=self.node_attributes_map,
                        edge_attributes=self.edge_attributes_map)
