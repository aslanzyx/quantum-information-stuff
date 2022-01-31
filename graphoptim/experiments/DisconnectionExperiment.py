import random
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from graphoptim.graph_state import ClusterState, GraphState


def count_connected(circuit_func, run_size, **prams) -> int:
    count = 0
    for i in range(run_size):
        if circuit_func(**prams):
            count += 1
    return count


def random_circuit1(m, n, density) -> bool:
    k = int(n * density)
    c = ClusterState(n)
    parity = 0
    for i in range(m):
        t_id = random.sample(range(n), k)
        for j in range(n):
            if j in t_id:
                c.t(j)
            else:
                gate_id = random.randint(0, 3)
                if gate_id == 0:
                    c.h(j)
                elif gate_id == 1:
                    c.x(j)
                elif gate_id == 2:
                    c.z(j)
                elif gate_id == 3:
                    c.s(j)
        if parity:
            for j in range(1, n - 1, 2):
                c.cnot(j, j + 1)
        else:
            for j in range(0, n - 1, 2):
                c.cnot(j, j + 1)
        parity ^= 1
    g = c.to_graph_state()
    g.eliminate_pauli()
    g.draw()
    plt.show()
    plt.clf()
    # print("connected") if check_connectivity(g) else print("disconnected")
    return check_connectivity(g)


def random_circuit2(m, n, density) -> float:
    k = int(n * density)
    c = ClusterState(n)
    parity = 0
    for i in range(m):
        t_id = random.sample(range(n), k)
        for j in range(n):
            if j in t_id:
                c.t(j)
            else:
                gate_id = random.randint(0, 3)
                if gate_id == 0:
                    c.h(j)
                elif gate_id == 1:
                    c.x(j)
                elif gate_id == 2:
                    c.z(j)
                elif gate_id == 3:
                    c.s(j)
        if parity:
            for j in range(1, n - 1, 2):
                c.cnot(j, j + 1)
        else:
            for j in range(0, n - 1, 2):
                c.cnot(j, j + 1)
        parity ^= 1
    g = c.to_graph_state()
    g.eliminate_pauli()
    # g.draw()
    # plt.show()
    # plt.clf()
    node_count = len(g.G.nodes())
    # print(count_max_connected_subgraph(g))
    # print(node_count)
    return count_max_connected_subgraph(g) / node_count


def check_connectivity(g: GraphState) -> bool:
    # Remove all the single node
    remove_disconnected_nodes(g)
    # Check connectivity
    nodes = list(g.G.nodes())
    if len(nodes) == 0:
        return False
    edge_traversal = list(nx.dfs_preorder_nodes(g.G, source=nodes[0]))
    return len(edge_traversal) == len(nodes)


def count_max_connected_subgraph(g: GraphState) -> int:
    # Remove all the single node
    remove_disconnected_nodes(g)
    # Check connectivity
    max_connectivity = 0
    nodes = list(g.G.nodes())
    while len(nodes) > 0:
        node_traversal = list(nx.dfs_preorder_nodes(g.G, source=nodes[0]))
        max_connectivity = max(max_connectivity, len(node_traversal))
        if len(node_traversal) > len(nodes) / 2:
            break
        for n in node_traversal:
            nodes.remove(n)
    return max_connectivity


def remove_disconnected_nodes(g: GraphState):
    nodes = list(g.G.nodes())
    for ni in nodes:
        if len(list(g.G.neighbors(ni))) == 0:
            g.G.remove_node(ni)


def experiment1():
    run_size = 20
    m = 20
    n = 100
    density_upper_bound = .3
    density_lower_bound = .1
    density_runs = 20
    density_space = np.linspace(density_lower_bound, density_upper_bound, density_runs)
    connection_rates = []
    for density in density_space:
        count = count_connected(random_circuit1, run_size, m=m, n=n, density=density)
        connection_rates.append(count / run_size)
        print(count / run_size)
    plt.scatter(density_space, connection_rates)
    plt.show()


if __name__ == '__main__':
    depth_space = range(5, 40, 2)
    size_space = range(10, 40, 2)
    exp_size = 5
    density = .8
    max_connectivity_rate: np.ndarray = np.zeros((len(depth_space), len(size_space)))
    i = 0
    for m in depth_space:
        j = 0
        for n in size_space:
            connectivity_rate = 0
            for l in range(exp_size):
                connectivity_rate += random_circuit2(m, n, density)
            connectivity_rate /= exp_size
            max_connectivity_rate[i, j] = connectivity_rate
            print("complete depth={}, size={}, density={}, connectivity={}".format(m, n, density, connectivity_rate))
            j += 1
        i += 1
    X, Y = np.meshgrid(depth_space, size_space)
    CS = plt.contour(X, Y, max_connectivity_rate.T)
    plt.colorbar(CS)
    plt.xlabel("circuit depth")
    plt.ylabel("circuit size")
    plt.title("T-gate density={}".format(density))
    plt.show()
