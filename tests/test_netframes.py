import netrunner as nr
from netrunner.models import NodeMap, EdgeMap
import networkx
from networkx import Graph
from networkx.algorithms import community

# set up test networks
nf = nr.read_csv('../data/character-deaths.csv',
                 nodes=['Name', 'Allegiances'],
                 links=[('Name', 'Allegiances')])

nf2 = nr.read_csv('../data/battles.csv',
                  nodes=['name', 'attacker_king', 'defender_king'],
                  links=[('name', 'attacker_king'), ('name', 'defender_king')])


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


def test_join_all():
    initial_length = len(nf.frame)
    nf.join_all(nf2, left_on='Name', right_on='defender_king')
    assert nf.node_columns == ['Name', 'Allegiances', 'name', 'attacker_king', 'defender_king']
    assert nf.edge_columns == [('Name', 'Allegiances'), ('name', 'attacker_king'), ('name', 'defender_king')]
    assert len(nf.frame) > initial_length


def test_apply_frame():
    nf_new = nr.read_csv('../data/character-deaths.csv',
                         nodes=['Name', 'Allegiances'],
                         links=[('Name', 'Allegiances')])
    nf_new.frame['Allegiances'] = nf_new.frame['Allegiances'].str.lower()
    nf_new.frame['Name'] = nf_new.frame['Name'].str.lower()
    nf_new.apply_dataframe()
    for node in nf_new.net.nodes:
        assert node.islower()
