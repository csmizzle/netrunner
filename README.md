# netrunner
let's run on some networks

---
NetFrames will be a very important piece of netrunner, giving upstream access to the flexibility of Pandas DataFrames and the downstream power to NetworkX Graph analytics in a concise API.
Netrunner allows you to quickly construct complex, multi-relational networks from columnar data.

---

### Usage

There are several ways to interact with `netrunner`. By using the columnar data from DataFrame,
we can seamlessly construct complex networks.
We will start with the `run` functionality.

```python
import netrunner

df = pd.read_csv('path_to_data')
nf = netrunner.run(df, draw=True)
```

By passing a dataframe to the `run` function with `draw=True`,
the user will be prompted with a simple guide to constructing a NetFrame.

We can also pass the node columns and relationships to `run` to construct the NetFrame upon instantiation.

```python
import netrunner

df = pd.read_csv('path_to_data')
nf = netrunner.run(df, nodes=['node1', 'node2'], links=[('node1', 'node2')])
```

---

### NetFrame API

A user can also access the low level `NetFrame`, using `add_nodes`, `add_edges`, and `populate_network`.

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
