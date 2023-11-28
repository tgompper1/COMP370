import argparse
import networkx as nx
import operator
import json

def parse_for_edges(data):
    edges = []
    if isinstance(data, dict):
        for key, items in data.items():
            for item in items:
                if isinstance(item, dict):
                    edges.extend([(key, subitem) for subitem in item])
                    edges.extend(parse_for_edges(item))
                else:
                    edges.append((key, item))

    return edges

def compute_network_stats(interaction_network_path, stats_path):
    network = open(interaction_network_path)
    network_open = json.load(network)

    edges = parse_for_edges(network_open)

    G = nx.from_edgelist(edges, create_using=nx.DiGraph)

    deg_centrality = nx.degree_centrality(G)
    sorted_deg = dict(sorted(deg_centrality.items(), key=operator.itemgetter(1)))
    deg_ponies = list(sorted_deg.keys())
    top_three_deg = deg_ponies[0:3]

    close_centrality = nx.closeness_centrality(G)
    sorted_close = dict(sorted(close_centrality.items(), key=operator.itemgetter(1)))
    close_ponies = list(sorted_close.keys())
    top_three_close = close_ponies[0:3]
    
    btwn_centrality = nx.betweenness_centrality(G)
    sorted_btwn = dict(sorted(btwn_centrality.items(), key=operator.itemgetter(1)))
    btwn_ponies = list(sorted_btwn.keys())
    top_three_btwn = btwn_ponies[0:3]

    stats = {
        "degree": top_three_deg,
        "closeness": top_three_close,
        "betweenness": top_three_btwn
    }

    with open(stats_path, 'w') as out:
        json.dump(stats, out)
    

def main():
    print("running...")
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest='interaction_network_json', help='path to interaction_network_json', metavar='<nteraction_network.json>')
    parser.add_argument('-o', dest='stats_json', help = 'output path to stats json file ', metavar='<stats.json>')
    
    args=parser.parse_args()

    interaction_network_path = args.interaction_network_json
    stats_path = args.stats_json
    
    compute_network_stats(interaction_network_path, stats_path)


if __name__ == "__main__":
    main()
