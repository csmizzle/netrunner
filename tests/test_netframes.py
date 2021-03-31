from alfred.netframe import NetFrame, NodeMap, EdgeMap
import pandas as pd
import networkx
from networkx import Graph

df = pd.read_csv('../data/character-deaths.csv')
nf = NetFrame(df)


def test_node_parsing():
    col_to_parse = ['Name', 'Allegiances']
    nf.format_nodes(col_to_parse, ignore_chars='None')
    nodes = nf.to_json()['nodes']
    assert isinstance(nodes, list)
    assert len(nodes) > 0


def test_edge_parsing():
    cols_to_edges = [('Name', 'Allegiances')]
    nf.format_edges(cols_to_edges)
    edges = nf.to_json()['links']
    assert isinstance(edges, list)
    assert len(edges) > 0


def test_merge_dicts():
    col_to_parse = ['Name', 'Allegiances']
    cols_to_edges = [('Name', 'Allegiances')]
    nf.format_nodes(col_to_parse, ignore_chars='None')
    nf.format_edges(cols_to_edges)
    json = nf.to_json()
    assert isinstance(json, dict)
    assert 'nodes' and 'links' in json.keys()


def test_node_map():
    col_to_parse = ['Name', 'Allegiances']
    nf.format_nodes(col_to_parse)
    node_map = nf.node_map
    assert isinstance(node_map, NodeMap)
    assert isinstance(node_map.map, dict)


def test_edge_map():
    cols_to_edges = [('Name', 'Allegiances')]
    nf.format_edges(cols_to_edges)
    edge_map = nf.edge_map
    assert isinstance(edge_map, EdgeMap)
    assert isinstance(edge_map.map, dict)


def test_graph():
    col_to_parse = ['Name', 'Allegiances']
    cols_to_edges = [('Name', 'Allegiances')]
    nf.format_nodes(col_to_parse, ignore_chars='None')
    nf.format_edges(cols_to_edges)
    nf.populate_network()
    assert isinstance(nf.graph, Graph)


def test_update_node_map():
    col_to_parse = ['Name', 'Allegiances']
    cols_to_edges = [('Name', 'Allegiances')]
    nf.format_nodes(col_to_parse)
    nf.format_edges(cols_to_edges)
    nf.populate_network()
    nf.update_node_map(nf.graph.degree(), 'degree')
    nf.update_node_map(networkx.degree_centrality(nf.graph), 'between')

    for node in nf.node_map.map.keys():
        assert 'degree' and 'between' in nf.node_map.map[node]['attributes'].keys()

    nf.update_node_map(networkx.eigenvector_centrality(nf.graph), 'eigenvector')

    for node in nf.node_map.map.keys():
        assert 'degree' and 'between' and 'eigenvector' in nf.node_map.map[node]['attributes'].keys()
