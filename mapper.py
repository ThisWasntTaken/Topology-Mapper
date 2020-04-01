import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import networkx as nx
from pyvis import network as net
from win32api import GetSystemMetrics

class Mapper:
    def __init__(self, data):
        self.data = data
        self.clusters = None

    @staticmethod
    def get_cover(domain, interval_len, overlap):
        domain_min = domain[0]
        domain_max = domain[1]
        cover = []
        upto_low, upto_high = domain_min, domain_min + interval_len
        while True:
            if upto_high >= domain_max:
                cover.append((upto_low, domain_max))
                break

            cover.append((round(upto_low, 2), round(upto_high, 2)))
            upto_low += (interval_len - overlap)
            upto_high += (interval_len - overlap)
        
        return cover

    def make_clusters(self, filter_func, cover, dbscan_algo):
        clusters = []
        for (low, high) in cover:
            to_cluster = list(filter(lambda p : filter_func(p, (low, high)), self.data))
            if not len(to_cluster):
                continue
            
            to_cluster = np.array(to_cluster)
            db = dbscan_algo.fit(to_cluster)
            labels = np.array(db.labels_)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            for i in range(0, n_clusters):
                clusters.append(set([tuple(p) for p in to_cluster[labels == i]]))
        
        self.clusters = clusters
        return clusters

    def create_graph(self, file_name):
        max_nodes = max([len(i) for i in self.clusters])
        g = net.Network(GetSystemMetrics(1), GetSystemMetrics(0), bgcolor="#222222")
        g.add_nodes(nodes = range(0, len(self.clusters), 1),
                    size = [len(x) / len(self.clusters) for x in self.clusters],
                    title = ["Contains " + str(len(x)) + " elements" for x in self.clusters],
                    label = [' '] * len(self.clusters),
                    color = ['#%02x%02x%02x' % (255, 255 - int(len(i) / max_nodes * 255), 0) for i in self.clusters])
        for i in range(0, len(self.clusters)):
            for j in range(i + 1, len(self.clusters)):
                if self.clusters[i].intersection(self.clusters[j]):
                    g.add_edge(i, j, color = '#ffdd00')
        
        g.set_options("""
        var options = {
        "nodes": {
            "shadow": {
            "enabled": true
            }
        },
        "edges": {
            "color": {
            "inherit": true
            },
            "smooth": false
        },
        "physics": {
            "barnesHut": {
            "centralGravity": 0,
            "springLength": 50,
            "springConstant": 0.01,
            "avoidOverlap": 0.5
            },
            "minVelocity": 0.75
        }
        }
        """)
        g.show(file_name)
        return g

if __name__ == "__main__":
    from sklearn.datasets import make_circles

    data = make_circles(n_samples=10000, noise=0.03, random_state=None, factor=0.3)[0]
    mapper = Mapper(data)
    cover = Mapper.get_cover(domain = (-1.3, 1.3), interval_len = 0.3, overlap = 0.1)

    dbscan_algo = DBSCAN(algorithm = 'auto', eps = 0.1, leaf_size = 30, metric = 'euclidean', min_samples = 3, p = None)
    def filter_func(p, interval):
        low, high = interval[0], interval[1]
        return (p[1] >= low and p[1] <= high)

    clusters = mapper.make_clusters(filter_func = filter_func, cover = cover, dbscan_algo = dbscan_algo)
    graph = mapper.create_graph(file_name = "example.html")