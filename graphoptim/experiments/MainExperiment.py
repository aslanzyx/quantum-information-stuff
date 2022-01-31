import matplotlib.pyplot as plt
import networkx as nx
from math import pi
from graphoptim.graph_state import ClusterState, GraphState
import random


def main():
    test_disconnect()


def test_disconnect():
    n = 40
    m = 40
    c = ClusterState(n)
    parity = 0
    for i in range(m):
        t_id = random.randint(0, n - 1)
        for j in range(n):
            if j == t_id:
                c.t(j)
            else:
                c.h(j)
        if parity:
            for j in range(1, n - 1, 2):
                c.cnot(j, j + 1)
        else:
            for j in range(0, n - 1, 2):
                c.cnot(j, j + 1)
        parity ^= 1
    g = c.to_graph_state()
    # g.eliminate_pauli()
    g.draw()
    plt.show()


def test_1():
    c = ClusterState(1)
    for i in range(10):
        c.h(0)
        c.t(0)
    for i in range(4):
        c.x(0)
        c.t(0)
    for i in range(5):
        c.h(0)
        c.t(0)
    for i in range(4):
        c.x(0)
        c.t(0)

    g = c.to_graph_state()
    g.eliminate_pauli()

    #  Another HT reduce
    g.local_complement((98, 0), 1)
    g.local_complement((92, 0), 1)
    g.local_complement((86, 0), 1)
    g.local_complement((80, 0), 1)
    g.local_complement((74, 0), 1)
    #  HT reduce
    g.local_complement((52, 0), 1)
    g.local_complement((46, 0), 1)
    g.local_complement((40, 0), 1)
    g.local_complement((34, 0), 1)
    g.local_complement((28, 0), 1)
    g.local_complement((22, 0), 1)
    g.local_complement((16, 0), 1)

    # Experimental
    #  g.local_complement((80, 0), 1)
    #  g.local_complement((74, 0), 1)
    #  g.local_complement((80, 0), 1)
    #  g.local_complement((74, 0), 1)

    # g.local_complement((86, 0), 1)
    # g.local_complement((74, 0), 1)

    # g.local_complement((92, 0), 1)
    # g.local_complement((86, 0), 1)
    # g.local_complement((92, 0), 1)
    #
    # g.local_complement((74, 0), 1)
    # g.local_complement((86, 0), 1)
    # g.local_complement((98, 0), 1)
    # g.local_complement((74, 0), 1)

    # # g.local_complement((86, 0), 1)
    # # g.local_complement((98, 0), 1)
    # # g.local_complement((80, 0), 1)
    #
    # # g.local_complement((98, 0), 1)
    # g.local_complement((58, 0), 1)
    # g.local_complement((98, 0), 1)

    g.draw_circular()
    # g.draw()
    plt.show()
    return c, g


def test_2():
    c = ClusterState(2)
    for i in range(8):
        c.x(0)
        c.z(0)
        c.t(0)
        c.h(1)
        c.t(1)
    c.cnot(0, 1)
    for i in range(8):
        c.h(0)
        c.t(0)
        c.h(1)
        c.t(1)
    g = c.to_graph_state()
    g.eliminate_pauli()

    g.local_complement((94, 1), 1)
    g.local_complement((88, 1), 1)
    g.local_complement((82, 1), 1)
    g.local_complement((76, 1), 1)
    g.local_complement((70, 1), 1)
    g.local_complement((64, 1), 1)
    g.local_complement((58, 1), 1)
    g.local_complement((46, 1), 1)
    g.local_complement((40, 1), 1)
    g.local_complement((34, 1), 1)
    g.local_complement((28, 1), 1)
    g.local_complement((22, 1), 1)
    g.local_complement((16, 1), 1)
    g.local_complement((10, 1), 1)
    g.local_complement((94, 0), 1)
    g.local_complement((88, 0), 1)
    g.local_complement((82, 0), 1)
    g.local_complement((76, 0), 1)
    g.local_complement((70, 0), 1)
    g.local_complement((64, 0), 1)
    g.local_complement((58, 0), 1)
    g.local_complement((46, 0), 1)
    g.local_complement((40, 0), 1)
    g.local_complement((34, 0), 1)
    g.local_complement((28, 0), 1)
    g.local_complement((22, 0), 1)
    g.local_complement((16, 0), 1)
    g.local_complement((10, 0), 1)

    # g.draw_circular()
    g.draw()
    plt.show()
    return c.g


def test_3():
    n = 7
    c = ClusterState(2)
    c.add_rotation_sequence(0, [0] * n)
    c.add_rotation_sequence(1, [0] * 2)
    g = c.to_graph_state()
    g.G.add_edge((1, 0), (1, 1))
    g.G.add_edge((2, 0), (1, 1))
    for i in range(2, n + 1):
        g.draw_circular()
        plt.show()
        g.local_complement((i, 0), 1)

    # g.local_complement((1, 1), 1)
    # g.local_complement((0, 1), 1)
    g.draw_circular()
    # g.draw()
    plt.show()


def test_4():
    """
    Test reduced CNOT gate
    :return:
    """
    c = ClusterState(2)
    c.add_rotation_sequence(0, [pi / 4] * 2)
    c.add_rotation_sequence(1, [pi / 4] * 2)
    c.cnot(0, 1)
    c.add_rotation_sequence(0, [pi / 4] * 2)
    c.add_rotation_sequence(1, [pi / 4] * 2)
    g = c.to_graph_state()
    g.eliminate_pauli()
    g.local_complement((1, 1), 1)
    g.local_complement((1, 0), 1)
    # g.draw_circular()
    g.draw()
    plt.show()


# Test cluster 3
n = 7
c = ClusterState(2)
c.add_rotation_sequence(0, [0] * n)
c.add_rotation_sequence(1, [0] * 4)
g = c.to_graph_state()
g.G.add_edge((1, 0), (2, 1))
g.G.add_edge((2, 0), (2, 1))

g.local_complement((0, 1), 1)
g.local_complement((1, 1), 1)
g.local_complement((2, 1), 1)
g.local_complement((3, 1), 1)
g.local_complement((4, 1), 1)
g.local_complement((2, 0), 1)
g.local_complement((3, 0), 1)
g.local_complement((4, 0), 1)
g.local_complement((5, 0), 1)
g.local_complement((6, 0), 1)
g.local_complement((7, 0), 1)
# g.local_complement((0, 0), 1)

# g.local_complement((1, 1), 1)
# g.local_complement((0, 1), 1)
# g.local_complement((1, 1), 1)
# for i in range(2, n + 1):
#     g.local_complement((i, 0), 1)
#
# g.local_complement((5, 0), 1)
# g.local_complement((3, 0), 1)
# g.local_complement((1, 0), 1)

# g.local_complement((2, 0), 1)
# g.local_complement((1, 0), 1)
# g.draw_circular()
# g.draw()
# plt.show()

# Test cluster 3
n = 4
c = ClusterState(2)
c.add_rotation_sequence(0, [0] * n)
c.add_rotation_sequence(1, [0] * n)
g = c.to_graph_state()
g.G.add_edge((2, 0), (2, 1))
g.local_complement((1, 0), 1)
g.local_complement((2, 0), 1)
g.local_complement((2, 1), 1)
g.local_complement((1, 1), 1)
g.local_complement((2, 0), 1)
# g.draw_circular()
# g.draw()
# plt.show()

# Test 4
n = 4
c = ClusterState(2)
c.add_rotation_sequence(0, [pi / 4] * n)
c.add_rotation_sequence(1, [pi / 4] * n)
g = c.to_graph_state()
g.G.add_edge((2, 0), (2, 1))
g.G.add_edge((2, 0), (3, 1))
g.local_complement((2, 0), 1)
g.local_complement((1, 1), 1)
g.local_complement((2, 1), 1)
g.local_complement((2, 0), 1)
g.local_complement((2, 1), 1)
g.local_complement((1, 1), 1)
g.local_complement((2, 1), 1)
g.local_complement((1, 0), 1)

#  g.draw_circular()
# g.draw()
# plt.show()


# Test cluster 5
c = ClusterState(3)
for i in range(3):
    c.h(0)
    c.t(0)
    c.h(1)
    c.t(1)
    c.h(2)
    c.t(2)
    c.cnot(0, 1)
    c.h(0)
    c.t(0)
    c.h(1)
    c.t(1)
    c.h(2)
    c.t(2)
    c.cnot(1, 2)
g = c.to_graph_state()
g.eliminate_pauli()
#  g.local_complement((40, 2), 1)
#  g.local_complement((28, 2), 1)
#  g.local_complement((10, 2), 1)
#  g.local_complement((52, 1), 1)
#  g.local_complement((40, 1), 1)
#  g.local_complement((28, 1), 1)
#  g.local_complement((16, 1), 1)
#  g.local_complement((40, 0), 1)
#  g.local_complement((34, 0), 1)
#  g.local_complement((22, 0), 1)
#  g.local_complement((16, 0), 1)
#  g.draw_circular()
#  g.draw()
#  plt.show()

# Test cluster 1
c = ClusterState(3)
for i in range(4):
    c.h(0)
    c.t(0)
    c.h(1)
    c.t(1)
    c.h(2)
    c.t(2)
    c.cnot(0, 1)
    c.cnot(1, 2)
g = c.to_graph_state()
g.eliminate_pauli()
g.local_complement((16, 2), 1)
g.local_complement((40, 1), 1)
#  g.draw()
#  plt.show()

if __name__ == "__main__":
    main()
