"""
Access Netrunner from top level init

"""

from netrunner.netframe import NetFrame, pd
from netrunner.utils import evaluate_draw
from typing import List, Tuple


def read_csv(path: str,
             nodes: list = None,
             links: List[Tuple] = None, **params) -> NetFrame:
    """
    Create Netframe directly from path
    Give users flexibility to use NetFrame right away or do work
    first

    :param path: str
        path to file
    :param nodes: list
        list of columns to make nodes from
    :param links:
        list of tuples acting as source / target mappings
    :param params:
    :return: Netframe
    """

    # TODO: Scrape pandas read_... to create class that will parse these arguments to give full access to the API

    df = pd.read_csv(path)

    # user input if None for nodes and edges
    # display info about dataframe
    draw = params.pop('draw', None)

    if not nodes or not links:

        eval_ = evaluate_draw(df, nodes=nodes, links=links, draw=draw)
        nodes, links = eval_.nodes, eval_.links

    # populate edges, nodes, and network
    return NetFrame(dataframe=df, nodes=nodes, links=links, **params)
