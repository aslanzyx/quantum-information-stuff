from typing import List, Set
import numpy as np


def parse_qasm(filename: str):
    f = open(filename)
    lines = f.readlines()
    pass


def remove_empty_lines(lines: List[str]):
    filter(lambda s: len(s) == 0, lines)
    return NotImplementedError()


class Circuit:
    def __init__(self) -> None:
        self.size = 0
        self.gate_stacks = []

    def parse(self):
        return NotImplementedError()


def top_order(dag: List[int], reverse: bool = False):
    '''
    Return the topological order of the given DAG.
    '''
    not_visited: set[int] = set(range(len(dag)))
    order: List[int] = []

    while len(not_visited) > 0:
        not_visited = not_visited.difference(
            dfs(dag, list(not_visited)[0], order.append))

    return order[::(-1)**(reverse ^ True)]


def dfs(dag: List[List[int]], root: int, f: any) -> Set[int]:
    '''
    Traverse the given DAG using DFS and return the visited node.
    dag: DAG denoted by edge lists
    root: the root node of the DFS tree
    f: post-order call-back function
    '''
    visited: Set[int] = set()

    def helper(node: int):
        visited.add(node)
        for next_node in dag[node]:
            if next_node not in visited:
                helper(next_node)
        f(node)

    helper(root)
    return visited


dag = [
    [1, 2, 3, 4],
    [3],
    [3, 4],
    [4],
    [],
    [6, 7, 8, 9],
    [8],
    [8, 9],
    [9],
    []
]

print(top_order(dag))


class ClusterModel:
    def __init__(self) -> None:
        self.size = 0
