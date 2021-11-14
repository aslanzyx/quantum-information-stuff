from graphoptim.graph_state import GraphState, Node, BlochSphere, ClusterState, PauliOperator
import graphviz

g = GraphState()
# T gate
g.add_node(Node('T', 0))
g.add_node(Node('X', 1))
g.add_edge(0, 1)
# Hadamard
g.add_node(Node('X', 2))
g.add_node(Node('Y', 3))
g.add_node(Node('Y', 4))
g.add_node(Node('Y', 5))
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(4, 5)
# CNOT
g.add_node(Node('X', 6))
g.add_node(Node('Y', 7))
g.add_node(Node('Y', 8))
g.add_node(Node('X', 9))
g.add_node(Node('Y', 10))
g.add_node(Node('Y', 11))
g.add_node(Node('X', 12))
g.add_node(Node('X', 13))
g.add_node(Node('X', 14))
g.add_node(Node('X', 15))
g.add_node(Node('X', 16))
g.add_node(Node('X', 17))
g.add_edge(6, 7)
g.add_edge(7, 8)
g.add_edge(8, 9)
g.add_edge(9, 10)
g.add_edge(10, 11)
g.add_edge(12, 13)
g.add_edge(13, 14)
g.add_edge(14, 15)
g.add_edge(15, 16)
g.add_edge(16, 17)
g.add_edge(9, 15)
# output
g.add_node(Node('Z', -1))
g.add_node(Node('Z', -2))
g.set_output(-1)
g.set_output(-2)

# connect T, H and CNOT
g.add_edge(1, 6)
g.add_edge(5, 12)
g.add_edge(11, -1)
g.add_edge(17, -2)

# connect output


# g.x_measurement(3, 1)
# print(g.edges)

# b = BlochSphere([1, 0, 0])
# b.rotate_sqrt_y(-1)
# print(b.vector)

# g.render()
p = PauliOperator('z')
# print(p)

c = ClusterState(4)
c.add_t(0)
c.add_t(1)
c.add_t(2)
c.add_t(3)
c.add_cnot(0, 1)
c.add_cnot(2, 3)
c.add_t(0)
c.add_t(1)
c.add_t(2)
c.add_t(3)
c.add_cnot(0, 3)
c.add_cnot(1, 2)
c.add_t(0)
c.add_t(1)
c.add_t(2)
c.add_t(3)
c.add_cnot(0, 1)
c.add_cnot(2, 3)
# print(c.operator_buffer)
# print(c.location_buffer)
c.finalize_buffer()
# print(c.corrections.items())

g = c.to_graph_state()
# g.render()
g.eliminate_pauli()
to = g.extract_topological_order()
print(to)
print([g.nodes[label] for label in to])
# g.render()
print("reached")
g.render_temporal_order()
# print(c.lines)

# g = graphviz.Graph()
# c = graphviz.Graph()
#
# g.node('a')
# g.node('b')
# g.node('c')
# c.edge('a', 'b')
# g.edge('a', 'c')
# g.subgraph(c)
# print(g)
# g.view()
# # g.render("graphviz_demo", view=True)

# from graphviz import Digraph
#
# g = Digraph('G', filename='cluster.gv')
#
# # NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
# #       so that Graphviz recognizes it as a special cluster subgraph
#
# with g.subgraph(name='cluster_0') as c:
#     c.attr(style='filled', color='lightgrey')
#     c.node_attr.update(style='filled', color='white')
#     # c.edges([('a0', 'a1'), ('a1', 'a2'), ('a2', 'a3')])
#     c.node('a0')
#     c.node('a1')
#     c.node('a2')
#     c.node('a3')
#     c.attr(label='process #1')
#
# with g.subgraph(name='cluster_1') as c:
#     c.attr(color='blue')
#     c.node_attr['style'] = 'filled'
#     c.edges([('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3')])
#     c.attr(label='process #2')
#
# g.edges([('a0', 'a1'), ('a1', 'a2'), ('a2', 'a3')])
# g.edge('start', 'a0')
# g.edge('start', 'b0')
# g.edge('a1', 'b3')
# g.edge('b2', 'a3')
# g.edge('a3', 'a0')
# g.edge('a3', 'end')
# g.edge('b3', 'end')
#
# g.node('start', shape='Mdiamond')
# g.node('end', shape='Msquare')
#
# g.view()
