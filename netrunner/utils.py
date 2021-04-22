"""
Utility functions for Netrunner

"""

from netrunner.models import DrawResults
from pandas.core.frame import DataFrame


def evaluate_draw(df: DataFrame, nodes=None, links=None, draw=None) -> DrawResults:
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

        if draw == 'y':
            answer = 'y'

        else:
            answer = 'n'

    if answer.lower() == 'y':

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
