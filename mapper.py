import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import networkx as nx
from pyvis import network as net
from win32api import GetSystemMetrics

class Mapper:
    def __init__(self, data):
        """
        Initialize the Mapper instance.

        Parameters:
        - data          : the data for which the mapper is defined

        Returns:
        - None
        """
        self.data = data
        self.clusters = None

    @staticmethod
    def get_cover(range_, interval_len, overlap):
        assert len(range_) == len(interval_len) == len(overlap), "Dimension mismatch!"
        cover = []
        for i in range(len(range_)):
            range_min = range_[i][0]
            range_max = range_[i][1]
            intervals = []
            upto_low, upto_high = range_min, range_min + interval_len[i]
            while True:
                if upto_high >= range_max:
                    intervals.append((upto_low, range_max))
                    break

                intervals.append((round(upto_low, 10), round(upto_high, 10)))
                upto_low += (interval_len[i] - overlap[i])
                upto_high += (interval_len[i] - overlap[i])
            
            cover.append(intervals)
        
        return cover

    def get_clusters(self, filter_func, cover, dbscan_algo):
        assert len(cover) == len(filter_func), "Dimension mismatch!"
        clusters = []
        
        def __get_clusters(filter_func, cover, _rec_num, _low, _high):
            if _rec_num < len(cover):
                for (low, high) in cover[_rec_num]:
                    _low[_rec_num], _high[_rec_num] = low, high
                    __get_clusters(filter_func, cover, _rec_num + 1, _low, _high)
            else:
                to_cluster = []
                for p in self.data:
                    flag = True
                    for i in range(len(_low)):
                        flag = flag and (filter_func[i](p) >= _low[i] and filter_func[i](p) <= _high[i])

                    if flag:
                        to_cluster.append(p)

                if len(to_cluster):
                    to_cluster = np.array(to_cluster)
                    db = dbscan_algo.fit(to_cluster)
                    labels = np.array(db.labels_)
                    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                    for i in range(0, n_clusters):
                        clusters.append(set([tuple(p) for p in to_cluster[labels == i]]))
        
        l = len(filter_func)
        __get_clusters(filter_func, cover, _rec_num = 0, _low = [0] * l, _high = [0] * l)
        self.clusters = clusters
        return clusters

    def create_graph(self, file_name):
        """
        Create, display and save a graph in pyvis.network.Network format

        Parameters:
        - file_name     : the name of the file to which the graph is to be saved

        Returns:
        - A graph, an instance of pyvis.network.Network
        """
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
            "smooth": true
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
    from sklearn.datasets import make_circles, make_blobs

    # data = make_circles(n_samples = 10000, noise = 0.03, random_state = None, factor = 0.5)[0]
    # mapper = Mapper(data)
    # cover = Mapper.get_cover(range_ = [(-1.3, 1.3)], interval_len = [0.3], overlap = [0.1])

    # dbscan_algo = DBSCAN(algorithm = 'auto', eps = 0.05, leaf_size = 30, metric = 'euclidean', min_samples = 3, p = None)
    
    # def filter_func_1(p):
    #     return p[1]

    # filter_func = [filter_func_1]
    # clusters = mapper.get_clusters(filter_func = filter_func, cover = cover, dbscan_algo = dbscan_algo)
    # graph = mapper.create_graph(file_name = "make_circles.html")

    data = make_blobs(n_samples = 5000, n_features = 5, random_state = 44)[0]
    mapper = Mapper(data)
    cover = Mapper.get_cover(range_ = [(-2, 13), (-12, 3)], interval_len = [2, 1], overlap = [0.5, 0.3])

    dbscan_algo = DBSCAN(algorithm = 'auto', eps = 1, leaf_size = 30, metric = 'euclidean', min_samples = 3, p = None)

    def filter_func_1(p):
        return p[0]

    def filter_func_2(p):
        return p[1]

    filter_func = [filter_func_1, filter_func_2]
    clusters = mapper.get_clusters(filter_func = filter_func, cover = cover, dbscan_algo = dbscan_algo)
    graph = mapper.create_graph(file_name = "make_blobs_5f_3b.html")