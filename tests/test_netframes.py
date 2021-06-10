import pandas as pd

import netrunner as nr
from netrunner.models import NodeMap, EdgeMap
from netrunner.netframe import NetFrame
import networkx
from networkx import Graph
from networkx.algorithms import community

# set up test networks
path = '../data/character-deaths.csv'
df_deaths = pd.read_csv(path)
path_battles = '../data/battles.csv'
df_battles = pd.read_csv(path_battles)

nf = nr.run(df_deaths,
            nodes=['Name', 'Allegiances'],
            links=[('Name', 'Allegiances')])

nf2 = nr.run(df_battles,
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
    nf_new = nr.run(df_deaths,
                    nodes=['Name', 'Allegiances'],
                    links=[('Name', 'Allegiances')])
    nf_new.frame['Allegiances'] = nf_new.frame['Allegiances'].str.lower()
    nf_new.frame['Name'] = nf_new.frame['Name'].str.lower()
    nf_new.apply_dataframe()
    for node in nf_new.net.nodes:
        assert node.islower()


def test_node_attributes():
    df = pd.read_csv('../data/battles.csv')
    netframe = NetFrame(df)
    nodes_cols = ['name', 'attacker_king']
    cols_to_edges = [('name', 'attacker_king')]
    node_attributes = {'name': ['year', 'region'], 'attacker_king': ['attacker_1']}
    netframe.add_nodes(nodes_cols)
    netframe.add_edges(cols_to_edges)
    netframe.set_node_attributes(node_attributes)
    for n in netframe.net.nodes:
        assert len(netframe.net.nodes[n]['attributes']) > 0


def test_edge_attributes():
    df = pd.read_csv('../data/battles.csv')
    netframe = NetFrame(df)
    nodes_cols = ['name', 'attacker_king']
    cols_to_edges = [('name', 'attacker_king')]
    edge_attributes = {('name', 'attacker_king'): ['attacker_outcome']}
    netframe.add_nodes(nodes_cols)
    netframe.add_edges(cols_to_edges)
    netframe.set_edge_attributes(edge_attributes)
    for e in netframe.net.edges:
        assert len(netframe.net.edges[e]['attributes']) > 0
