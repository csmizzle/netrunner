# netrunner
let's run on some networks

NetFrames will be a very important piece of netrunner, giving upstream access to the flexibility of Pandas DataFrames and the downstream power to NetworkX Graph analytics in a conscise API.

### Usage

NetFrames allow a user to simply pass a DataFrame object to NetFrame and started.

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
