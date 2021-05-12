"""
Access Netrunner from top level init

"""

from netrunner.netframe import NetFrame, DataFrame
from netrunner.utils import evaluate_draw
from typing import List, Tuple


def run(df: DataFrame,
        nodes: list = None,
        links: List[Tuple] = None, **params) -> NetFrame:
    """
    Create Netframe directly from path
    Give users flexibility to use NetFrame right away or do work
    first

    :param df: DataFrame
        DataFrame to create netframe from
    :param nodes: list
        list of columns to make nodes from
    :param links:
        list of tuples acting as source / target mappings
    :param params:
    :return: Netframe
    """

    # user input if None for nodes and edges
    # display info about dataframe
    draw = params.pop('draw', False)

    if not nodes or not links:

        eval_ = evaluate_draw(df, nodes=nodes, links=links, draw=draw)
        nodes, links = eval_.nodes, eval_.links

    # populate edges, nodes, and network
    return NetFrame(dataframe=df, nodes=nodes, links=links, **params)
