"""Class for handling graphs"""

class Graph:
    """Graph class for handling graphs"""

    class Node:
        """Simple node for graph"""

        def __init__(self, node_id: int, node_value):
            """initializing the object"""
            self.value = node_value
            self.node_id = node_id
            self.connections = []

        def add_node_connection(self, node, weight):
            """Add a new connection with weight"""
            self.connections += [(node, weight)]

        def get_connections(self):
            """Get all connection from this node"""
            return self.connections

    def __init__(self):
        """Initializing the object"""
        self.nodes = {}

    def add_node(self, graph_node):
        """Add a new node to the graph"""
        self.nodes[graph_node.node_id] = graph_node

    def exist_node(self, graph_node):
        """Check if a node exists"""
        return self.nodes[graph_node.node_id] is not None

    def get_node(self, id1):
        """Get a node with a specified id"""
        return self.nodes[id1]

    def add_arch(self, from_node, to_node, weight):
        """Add a new arch between two nodes"""
        if self.exist_node(from_node):
            self.add_node(to_node)
            from_node.add_node_connection(to_node, weight)

    def deep_first_search(self):
        """Deep first search"""
        for node in self.nodes:
            string = f'{node} -> '
            for connection in self.nodes[node].connections:
                string += f'{connection[0].node_id} '
            print(string)
            # print(self.nodes[node])

    def evaluate_costs(self, id1):
        """From the given id evaluate every possible path
        form the given node to the others with minimun cost"""
        costs = {node: 9999 for node in self.nodes}
        parents = {node: None for node in self.nodes}

        costs[id1] = 0

        for node in self.nodes:
            for next_node, weight in self.nodes[node].connections:
                if costs[node] + weight < costs[next_node.node_id]:
                    costs[next_node.node_id] = costs[node] + weight
                    parents[next_node.node_id] = node

        return parents, costs

    def find_path(self, id1, id2):
        """Find path from node id1 to node id2"""
        parents, _ = self.evaluate_costs(id1)
        node_id = id2
        path = []
        while parents[node_id] is not None:
            node_id = parents[node_id]
            path = [node_id] + path
        return path + [id2]
