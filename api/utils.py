import os


def get_environment():
    if os.environ.get('ENVIRONMENT') is None:
        return 'DEV'
    else:
        return os.environ['ENVIRONMENT']


def get_subgraph_endpoint():
    env = get_environment()
    if env == 'DEV':
        return 'https://api.thegraph.com/subgraphs/name/hashink/rinkeby'
    elif env == 'TEST':
        return 'https://api.thegraph.com/subgraphs/name/hashink/rinkeby'
    else:
        return 'https://api.thegraph.com/subgraphs/name/hashink/rinkeby'
