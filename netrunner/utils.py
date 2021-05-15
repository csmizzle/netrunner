"""
Utility functions for Netrunner

"""

from netrunner.models import DrawResults, Node
from pandas.core.frame import DataFrame
from typing import List, Tuple


# small wrapper for draw argument -- will be helpful when UI is created
def evaluate_draw(df: DataFrame, nodes: list = None, links: list = None, draw: bool = None) -> DrawResults:
    """
    Evaluate draw parameter

    :param df:
    :param nodes:
    :param links:
    :param draw:
    :return:
    """

    # evaluate user input on network creation
    if not draw:
        answer = input('Do you wish to format your network now? Y/N ')

    else:

        if draw is True:
            answer = True

        else:
            answer = False

    if answer is True:

        if not nodes:
            print("[*] Let's select which columns you want to use as nodes first ...")
            print('---DataFrame information---')
            print(df.info())
            print('---DataFrame Columns---\n', ', '.join(df.columns).strip(', '))
            nodes = input('[!] Enter Node Columns (separated by commas please)\n')
            nodes = nodes.split(', ')

        if not links:
            print("[*] Next, let's decide which columns you want to link together with edges.")
            print('[?] Nodes:', ', '.join(nodes))
            links = input('[!] Enter Links (node_1 -> node_2, node_2 -> node_3)\n')
            links = [(rel.split(' -> ')[0], rel.split(' -> ')[1]) for rel in links.split(', ')]

    return DrawResults(nodes=nodes, links=links)


# unpack source columns from NodeMap
def unpack_source_col(node: Node, node_map) -> List[Node]:
    """
    Unpack listed values from source_col in NodeMap.map

    :param node:
    :param node_map:
    :return:
    """

    if len(node_map[node]['source_col']) == 1:
        return [Node(name=node,
                     attributes=node_map[node]['attributes'],
                     source_col=node_map[node]['source_col'][0])]

    elif len(node_map[node]['source_col']) > 1:
        return [Node(name=node,
                     attributes=node_map[node]['attributes'],
                     source_col=col) for col in node_map[node]['source_col']]
