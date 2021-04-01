from netrunner.netframe import *
import networkx
from networkx import Graph
from networkx.algorithms import community

# set up test networks
df = pd.read_csv('../data/character-deaths.csv')
nodes_ = ['Name', 'Allegiances']
links_ = [('Name', 'Allegiances')]
nf = NetFrame(df, nodes=nodes_, links=links_)

df2 = pd.read_csv('../data/battles.csv')
nodes_cols = ['name', 'attacker_king', 'defender_king']
cols_to_edges = [('name', 'attacker_king'), ('name', 'defender_king')]
nf2 = NetFrame(df2, nodes=nodes_cols, links=cols_to_edges)


def test_node_parsing():
    nodes = nf.to_json()['nodes']
    assert isinstance(nodes, list)
    assert len(nodes) > 0


def test_edge_parsing():
    edges = nf.to_json()['links']
    assert isinstance(edges, list)
    assert len(edges) > 0


def test_merge_dicts():
    json = nf.to_json()
    assert isinstance(json, dict)
    assert 'nodes' and 'links' in json.keys()


def test_node_map():
    node_map = nf.node_map
    assert isinstance(node_map, NodeMap)
    assert isinstance(node_map.map, dict)


def test_edge_map():
    edge_map = nf.edge_map
    assert isinstance(edge_map, EdgeMap)
    assert isinstance(edge_map.map, dict)


def test_graph():
    assert isinstance(nf.net, Graph)


def test_update_node_map_degree():
    nf.update_node_map(nf.net.degree(), 'degree')
    for node in nf.node_map.map.keys():
        assert 'degree' in nf.node_map.map[node]['attributes'].keys()


def test_update_node_map_between():
    nf.update_node_map(networkx.degree_centrality(nf.net), 'between')
    for node in nf.node_map.map.keys():
        assert 'between' in nf.node_map.map[node]['attributes'].keys()


def test_update_node_map_eigen():
    nf.update_node_map(networkx.eigenvector_centrality(nf.net), 'eigenvector')
    for node in nf.node_map.map.keys():
        assert 'eigenvector' in nf.node_map.map[node]['attributes'].keys()


def test_update_node_map_community():
    nf.update_node_map(community.greedy_modularity_communities(nf.net), 'community')
    for node in nf.node_map.map.keys():
        assert 'community' in nf.node_map.map[node]['attributes'].keys()


def test_join():
    initial_length = len(nf.node_map.map.keys())
    nf.join_graph(nf2)
    assert len(nf.node_map.map.keys()) > initial_length


def test_join_all():
    initial_length = len(nf.frame)
    nf.join_all(nf2, left_on='Name', right_on='defender_king')
    assert len(nf.frame) > initial_length
