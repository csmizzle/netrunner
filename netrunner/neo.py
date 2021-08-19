"""
Map a netframe object to cypher and create entries to existing database
Mon both NodeMaps and EdgeMaps to Neo4j database
Will use Bulk operations for now and predefined structures from
NetFrame

"""
from netrunner.netframe import NetFrame
from py2neo import Graph
from py2neo.bulk import create_nodes


class NeoMapper:
    """
    Map NetFrame Nodes and Edges to Neo4j graph

    """

    def __init__(self,
                 graph: Graph,
                 netframe: NetFrame,
                 *args,
                 **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.graph = graph
        self.netframe = netframe
        self.node_labels = kwargs.pop('node_labels', None)
        self.edge_labels = kwargs.pop('edge_labels', None)

    def format_nodes(self) -> list:
        """
        Create node label from NodeMapping object
        """

        formatted_nodes = list()

        # use default mappings from Netframe in node_labels are not present
        if not self.node_labels:

            for node, attrs in self.netframe.node_map.map.items():

                for col in self.netframe.node_map.map[node]['source_col']:
                    node_entry = {
                        **{col: node},
                        **self.netframe.node_map.map[node]['attributes']
                    }
                    formatted_nodes.append(node_entry)

        # group source cols into node labels
        else:

            for node, attrs in self.netframe.node_map.map.items():

                for key, value in self.node_labels.items():

                    # check if source col needs to be mapped to node label
                    inter = list(set(self.netframe.node_map.map[node]['source_col']) & set(value))

                    # map to node label when entering node into Neo4j
                    if len(inter) > 0:

                        node_entry = {
                            **{key: node},
                            **self.netframe.node_map.map[node]['attributes']
                        }
                        formatted_nodes.append(node_entry)

                    else:

                        for col in self.netframe.node_map.map[node]['source_col']:

                            node_entry = {
                                **{col: node},
                                **self.netframe.node_map.map[node]['attributes']
                            }
                            formatted_nodes.append(node_entry)

        return formatted_nodes

