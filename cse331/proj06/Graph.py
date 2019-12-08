"""
Graph.py
Author: Ian Thompson
04/12/2019
"""

from collections import defaultdict
import math


class Graph:
    """
    A class to build a weighted graph
    Uses a nested dictionary to hold edges and weights
    """
    def __init__(self, n):
        """
        Constructor
        :param n: Number of vertices
        """
        self.order = n
        self.size = 0
        # You may put any required initialization code here
        self.graph = defaultdict(dict)  # Nested dictionary
        for x in range(0, n):
            self.graph[x] = dict()

    def insert_edge(self, u, v, w):
        """
        Inserts edge between vertices
        Raises index error if either vertex is not in graph
        :param u: First vertex
        :param v: Second vertex
        :param w: Weight
        """
        if u < self.order and v < self.order:  # Vertexes in graph
            if self.are_connected(u, v):
                self.size -= 1  # Edge will be replaced
            self.graph[u][v] = w
            self.graph[v][u] = w
            self.size += 1
        else:
            raise IndexError

    def degree(self, v):
        """
        Calculates degree of a vertex
        :param v: Vertex
        :return: Number of edges attached to v
        """
        if v < self.order:  # Vertex in graph
            return len(self.graph[v])
        else:
            raise IndexError

    def are_connected(self, u, v):
        """
        Determines if one edge connects two vertices
        :param u: First vertex
        :param v: Second vertex
        :return: If one edge connects v and u
        """
        if u < self.order and v < self.order:  # Both vertices in graph
            return v in self.graph[u].keys()
        else:
            raise IndexError

    def is_path_valid(self, path):
        """
        Uses are_connected to test input path
        :param path: Path to be tested
        :return: If the path is valid
        """
        prev = path[0]  # Start of path
        for item in path:
            if item != prev:
                if not self.are_connected(prev, item):
                    return False
            prev = item
        return True

    def edge_weight(self, u, v):
        """
        Weight between to vertices
        :param u: First vertex
        :param v: Second vertex
        :return: Weight of edge between them
        """
        if self.are_connected(u, v):
            return self.graph[u][v]
        return math.inf  # Not directly connected

    def path_weight(self, path):
        """
        Finds weight of given path
        :param path: Input path
        :return: Total weight
        """
        total_weight = 0
        prev = path[0]  # Start
        for item in path:
            if item != prev:
                total_weight += self.edge_weight(prev, item)
            prev = item
        return total_weight

    def does_path_exist(self, u, v):
        """
        Uses a breadth first search to find if a path exists
        :param u: Start vertex
        :param v: Ending vertex
        :return: If a path exists
        """
        if u >= self.order or v >= self.order:  # Start and end are in graph
            raise IndexError
        discovered = list()
        queue = list()
        queue.append(u)  # Start

        while queue:
            vertex = queue.pop(0)  # Dequeue next item
            if vertex == v:  # Ending vertex found
                return True
            for item in self.graph[vertex].keys():  # Enqueue all non-visited items
                if item not in discovered:
                    queue.append(item)
                    discovered.append(item)
        return False

    def find_min_weight_path(self, u, v):
        """
        Uses Dijkstra's algorithm to find lowest weight path
        :param u: Starting vertex
        :param v: Ending vertex
        :return: Path of lowest weight
        """

    def is_bipartite(self):
        """
        Determines if a graph is bipartite
        :return:
        """

