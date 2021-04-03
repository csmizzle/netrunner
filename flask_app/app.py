from netrunner.netframe import NetFrame
from flask import Flask, render_template
import pandas as pd
import json
import numpy as np

app = Flask(__name__)

# load sample data
df = pd.read_csv('../data/battles.csv')
nodes_cols = ['name', 'attacker_king', 'defender_king']
cols_to_edges = [('name', 'attacker_king'), ('name', 'defender_king')]
nf = NetFrame(df, nodes=nodes_cols, links=cols_to_edges)


@app.route('/')
def landing():
    return 'Welcome to Netrunner!'


@app.route('/get_columns')
def get_columns():
    return render_template("graph_creation.html", df=nf.frame)


@app.route('/get_degree')
def get_degree():
    return str(nf.net.degree())


@app.route('/render_network')
def draw_graph():
    json_data = nf.to_json()
    return render_template('graph.html', json_data=json.dumps(json_data))


if __name__ == "__main__":
    app.run('127.0.0.1', port=5000, debug=True)
