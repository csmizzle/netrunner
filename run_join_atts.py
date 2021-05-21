from netrunner.netframe import NetFrame
import networkx as nx
import pandas as pd

# create dataframes
deaths = pd.read_csv('./data/character-deaths.csv')
battles = pd.read_csv('./data/battles.csv')

# create maps
deaths_map = dict(nodes=['Name', 'Allegiances'],
                  links=[('Name', 'Allegiances')],
                  node_attributes={'Name': ['Gender', 'Nobility']})

battles_map = dict(nodes=['name', 'attacker_king', 'defender_king',
                          'attacker_commander', 'defender_commander'],
                   links=[('name', 'attacker_king'), ('name', 'defender_king'),
                          ('attacker_king', 'attacker_commander'), ('defender_king', 'defender_commander')],
                   node_attributes={'name': ['year', 'battle_number'],
                                    'attacker_king': ['attacker_outcome', 'attacker_size'],
                                    'defender_king': ['defender_size'],
                                    'defender_commander': ['defender_size'],
                                    'attacker_commander': ['attacker_size']})

# create netframes
nf_deaths = NetFrame(deaths, **deaths_map)
nf_battles = NetFrame(battles, **battles_map)
df = nx.to_pandas_edgelist(nf_battles.net)
print('Node Edge List:\n', df.head())

for n in nf_battles.net.nodes:
    print(f'{n}', nf_battles.net.nodes[n])

nf_battles.frame['attacker_commander'] = nf_battles.frame['attacker_commander'].str.split(', ')
nf_battles.frame = nf_battles.frame.explode('attacker_commander')
nf_battles.frame['defender_commander'] = nf_battles.frame['defender_commander'].str.split(', ')
nf_battles.frame = nf_battles.frame.explode('defender_commander')

print(nf_battles.frame)
print(nf_battles.node_attributes_map)
nf_battles.apply_dataframe()
nf_battles = nf_battles.apply_map()

for n in nf_battles.net.nodes:
    print(f'Node: {n}', nf_battles.net.nodes[n])

print('Node Cols:', nf_battles.node_columns)
print('Edge Cols:', nf_battles.edge_columns)
print('Node Attributes:', nf_battles.node_attributes_map)


nf_battles.join_graph(nf_deaths)
for n in nf_battles.net.nodes:
    print(f'Node: {n}', nf_battles.net.nodes[n])

print(nf_battles.node_map.map)