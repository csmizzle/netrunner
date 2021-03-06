# netrunner
let's run on some networks

---
NetFrames are essential to netrunner, giving upstream access to the flexibility of Pandas DataFrames and the downstream power to NetworkX Graph analytics in a concise API.
Netrunner allows you to quickly construct complex, multi-relational networks from columnar data.

---

### Usage

There are several ways to interact with `netrunner`. By using the column names from a pandas DataFrame,
we can seamlessly construct complex networks.
We will start with the `run` functionality, which helps us map DataFrame columns to network attributes.

```python
import netrunner
import pandas as pd

df = pd.read_csv('path_to_data')
nf = netrunner.run(df, draw=True)
```

By passing a dataframe to the `run` function with `draw=True`,
the user will be prompted with a simple guide to constructing a NetFrame.

We can also pass the node columns and relationships to `run` to construct the NetFrame upon instantiation.
After creation, the user now has access to the DataFrame and NetworkX Graph object all in one convenient place.

#### NetFrame Creation Syntax
- `nodes` - Nodes within the Networkx graph
  - list of column names
- `links` - Source/Edge links within Networkx graph
  - tuple of column names Ex: `[('source_col', 'target_col')]`
- `node_attributes` - Node attributes within Networkx graph
  - dictionary with node column to list of node attributes for given column
- `edge_attributes` - Edge attributes within Networkx graph
  - dictionary with node column to list of edge attributes for given column

```python
import netrunner
import pandas as pd

df = pd.read_csv('path_to_data')
nf = netrunner.run(df, nodes=['node1', 'node2'], links=[('node1', 'node2')])
print(nf.net.nodes)  # NetworkX Graph
print(nf.frame.head())  # DataFrame
```

### Network Maps
Network maps provide an easy any pythonic way of declaring graph structure that can easily be feed to `netrunner`,
consisting of four main keys within a Python dictionary.

Let's use the famous Game of Thrones dataset as an example.

```python
from netrunner.netframe import NetFrame
import pandas as pd

# create dataframes
deaths = pd.read_csv('character-deaths.csv')
battles = pd.read_csv('battles.csv')

# create maps using data frame columns
deaths_map = dict(nodes=['Name', 'Allegiances'],
                  links=[('Name', 'Allegiances')],
                  node_attributes={'Name': ['Gender', 'Nobility']})

battles_map = dict(nodes=['name', 'attacker_king', 'defender_king',
                          'attacker_commander', 'defender_commander'],
                   links=[('name', 'attacker_king'),
                          ('name', 'defender_king'),
                          ('attacker_king', 'attacker_commander'),
                          ('defender_king', 'defender_commander')],
                   node_attributes={'name': ['year', 'battle_number'],
                                    'attacker_king': ['attacker_outcome', 'attacker_size'],
                                    'defender_king': ['defender_size'],
                                    'defender_commander': ['defender_size'],
                                    'attacker_commander': ['attacker_size']},
                   edge_attributes={('name', 'attacker_king'): ['attacker_outcome']})

# create netframes using the maps as ** parameters
nf_deaths = NetFrame(deaths, **deaths_map)
nf_battles = NetFrame(battles, **battles_map)
```

---

### NetFrame API

A user can also access the low level `NetFrame`, using `add_nodes`, `add_edges`, `set_node_attributes`,
`set_edge_attributes`, and `populate_network`.

```python
from netrunner.netframe import NetFrame
nf = NetFrame(df)

# specifiy node columns
nodes = ['node_col']
# specifiy edge source / target columns
edges = [('source_col', 'edge_col')]

# populate nodes, edges, and network
nf.add_nodes(nodes)
nf.add_edges(edges)
nf.populate_nework()
```

If you already know which columns you want as nodes and edges, you can also specifiy these as parameters upon creation of your NetFrame.
```python
nf = NetFrame(df, nodes=['node_col', 'node_col_2'], links=[('node_col', 'node_col2')])
```
