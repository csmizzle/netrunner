"""
Map a netframe object to cypher and create entries to existing database
Mon both NodeMaps and EdgeMaps to Neo4j database
Will use Bulk operations for now and predefined structures from
NetFrame

"""
from netrunner.netframe import NetFrame
from netrunner.exceptions import EmptyEdgeLabelException
from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships


class NeoMapper:
    """
    Map NetFrame Nodes and Edges to Neo4j graph
    TODO: Duplicates still being created, get rid of those, maybe switch to merge?? Review LinkedKnowledge code
    TODO: for merging
    """

    def __init__(self,
                 graph: Graph,
                 netframe: NetFrame,
                 edge_labels: dict = None,
                 *args,
                 **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.graph = graph
        self.netframe = netframe
        self.edge_labels = edge_labels
        self.node_labels = kwargs.pop('node_labels', {})

    def _apply_node_labels(self, node_batches: dict):
        """
        Apply node labels to node batches
        :param node_batches: dict
        :return:
        """

        for key in self.node_labels:

            for column in self.node_labels[key]:

                if column in node_batches:

                    if key in node_batches:

                        node_batches[key].extend(node_batches.pop(column))

                    else:

                        node_batches[key] = node_batches.pop(column)

    # node operations
    def create_node_batches(self) -> dict:
        """
        Create node batches for py2neo bulk transactions
        These are looking to group by Node Labels into a dict with node label as key
        and node values as elements in a list
        :return: dict
        """

        batches_by_label = dict()

        for node in self.netframe.node_map.map:

            for col in self.netframe.node_map.map[node]['source_col']:

                if col:

                    if col not in batches_by_label.keys():
                        batches_by_label.update({
                            col: [
                                {**{'name': node}, **self.netframe.node_map.map[node]['attributes']}
                            ]
                        })

                    else:
                        batches_by_label[col].append(
                            {**{'name': node}, **self.netframe.node_map.map[node]['attributes']}
                        )

        # apply node labels if needed
        if len(self.node_labels) > 0:
            self._apply_node_labels(batches_by_label)

        return batches_by_label

    def insert_nodes(self) -> None:
        """
        Insert nodes into graph
        """
        batches = self.create_node_batches()
        for batch in batches:
            print(f'Creating {batch} nodes ...')
            create_nodes(
                self.graph.auto(),
                batches[batch],
                labels={batch},
            )

    def _check_node_labels(self, label) -> str:
        """
        check if label in node label
        :param label: str
        :return: str
        """
        if len(self.node_labels) > 0:
            for key in self.node_labels:
                if label in self.node_labels[key]:
                    return key
                else:
                    continue
            return label

    # edge operations
    def create_edge_batches(self) -> dict:
        """
        Create edge batches from EdgeMap
        Source columns need to match if node labels are present
        Example:
        data = {
            ((source_col, 'name'), (target_col, 'name')):
                [(key[0], flat_attrs, key[1]),
                ...]
        }
        :return: dict
        """

        edges = dict()

        for edge in self.netframe.edge_map.map:

            # create edge key for checking logic
            # check if node labels need to be applied
            source_col = self._check_node_labels(self.netframe.edge_map.map[edge]['source_col'])
            target_col = self._check_node_labels(self.netframe.edge_map.map[edge]['target_col'])

            edge_key = (
                (source_col, 'name'),
                (target_col, 'name')
            )

            if edge_key not in edges:

                edges.update({
                    edge_key: [
                        (
                            edge[0],
                            self.netframe.edge_map.map[edge]['attributes'],
                            edge[1]
                        )
                    ]
                })

            else:

                edges[edge_key].append(
                    (
                        edge[0],
                        self.netframe.edge_map.map[edge]['attributes'],
                        edge[1]
                    )
                )

        return edges

    def insert_edges(self) -> None:
        """
        Insert edges to Neo4j
        """
        edges_batches = self.create_edge_batches()
        _que_edge_labels = list()
        for batch in edges_batches:
            edge_key = (batch[0][0], batch[1][0])
            if edge_key in self.edge_labels.keys():
                print(edge_key)
                _que_edge_labels.append(self.edge_labels[edge_key])
            else:
                raise EmptyEdgeLabelException(edge_key)
        for batch, label in zip(edges_batches, _que_edge_labels):
            print(f'Creating relationships for edge {label} ...')
            create_relationships(
                self.graph.auto(),
                edges_batches[batch],
                label,
                start_node_key=batch[0],
                end_node_key=batch[1]
            )
