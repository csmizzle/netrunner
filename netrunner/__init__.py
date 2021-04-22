"""
Access Netrunner from top level init

"""

from netrunner.netframe import NetFrame, pd
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

    # populate edges, nodes, and network
    return NetFrame(dataframe=df, nodes=nodes, links=links, **params)
