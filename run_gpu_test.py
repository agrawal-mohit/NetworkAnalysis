import datetime
import time

from api_undirected_gpu import UndirectedNetworkAnalysis
from generate_edges import generate_edges
from generate_nodes import generate_nodes

node_count = 1000
edge_count = 10000

measure_generate_nodes = True
measure_generate_edges = True
measure_add_nodes = True
measure_add_edges = True

measure_get_result = True

if __name__ == '__main__':
    if measure_generate_nodes:
        start = time.time()
        generate_nodes(node_count)
        time_generate_nodes = time.time() - start
    else:
        time_generate_nodes = 0

    if measure_generate_edges:
        start = time.time()
        generate_edges(edge_count)
        time_generate_edges = time.time() - start
    else:
        time_generate_edges = 0

    analysis = UndirectedNetworkAnalysis()

    if measure_add_nodes:
        start = time.time()
        analysis.add_nodes("nodes.csv")
        time_add_nodes = time.time() - start
    else:
        time_add_nodes = 0

    if measure_add_edges:
        start = time.time()
        analysis.add_edges("edges.csv")
        time_add_edges = time.time() - start
    else:
        time_add_edges = 0
    print("add edges done")

    if measure_get_result:
        dt1 = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)
        dt2 = datetime.datetime(2100, 12, 31, 23, 59, 59, 0)
        start = time.time()
        analysis.get_result([], [], [], [], 100, dt1.date(), dt1.time(), dt2.date(), dt2.time())
        time_get_result = time.time() - start
    else:
        time_get_result = 0

    print(time_generate_nodes, " seconds to generate nodes")
    print(time_generate_edges, " seconds to generate edges")
    print(time_add_nodes, " seconds to add nodes")
    print(time_add_edges, " seconds to add edges")
    print(time_get_result, " seconds to get result")

