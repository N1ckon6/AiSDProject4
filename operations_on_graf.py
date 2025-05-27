import random
from collections import defaultdict

class GraphGenerator:
    def __init__(self):
        self.graph = defaultdict(list)
        self.num_nodes = 0
        self.saturation = 0
        self.mode = ""
    
    def add_edge(self, u, v):
        if v not in self.graph[u]:
            self.graph[u].append(v)
        if u not in self.graph[v]:
            self.graph[v].append(u)
    
    def generate_hamiltonian_graph(self, num_nodes, saturation):
        self.num_nodes = num_nodes
        self.saturation = saturation
        self.mode = "hamilton"
        
        if num_nodes <= 10:
            print("Error: Number of nodes must be greater than 10 for Hamiltonian graph.")
            return
        
        # Create a Hamiltonian cycle
        nodes = list(range(1, num_nodes + 1))
        random.shuffle(nodes)
        
        for i in range(num_nodes):
            self.add_edge(nodes[i], nodes[(i + 1) % num_nodes])
        
        # Calculate target number of edges
        max_possible_edges = num_nodes * (num_nodes - 1) // 2
        target_edges = int(max_possible_edges * saturation / 100)
        current_edges = num_nodes
        
        # Add edges while maintaining even degrees
        while current_edges < target_edges:

            u = random.randint(1, num_nodes)
            neighbors = self.graph[u]
            
            # Find two not connected nodes yet
            available = [v for v in range(1, num_nodes + 1) 
                        if v != u and v not in neighbors]
            
            if len(available) >= 2:
                v, w = random.sample(available, 2)
                if w not in self.graph[v]:
                    self.add_edge(u, v)
                    self.add_edge(u, w)
                    self.add_edge(v, w)
                    current_edges += 3
    
    def generate_non_hamiltonian_graph(self, num_nodes):
        self.num_nodes = num_nodes
        self.saturation = 50 
        self.mode = "non-hamilton"
        
        # Create a Hamiltonian graph
        self.generate_hamiltonian_graph(num_nodes, 50)
        
        # Isolate one node to make it non-hamiltonian
        if num_nodes > 1:
            node_to_isolate = random.randint(1, num_nodes)
            self.graph[node_to_isolate] = []  # remove all edges
            
            # Also remove references to this node from other nodes
            for node in self.graph:
                if node_to_isolate in self.graph[node]:
                    self.graph[node].remove(node_to_isolate)
    
    def print_graph(self):
                
        print("\nAdjacency list:")
        for node in sorted(self.graph.keys()):
            print(f"{node}: {sorted(self.graph[node])}")
        
        # Show node degrees
        print("\nNode degrees:")
        for node in sorted(self.graph.keys()):
            print(f"Node {node}: {len(self.graph[node])}")

    def is_eulerian(self):
        """Check if the graph is Eulerian (all vertices have even degree)"""
        for node in self.graph:
            if len(self.graph[node]) % 2 != 0:
                return False
        return True
    
    def find_eulerian_cycle(self):
        """Find an Eulerian cycle using Hierholzer's algorithm"""
        if not self.is_eulerian():
            print("Graph is not Eulerian (not all vertices have even degree)")
            return None
        
        # Make a copy of the graph to work with
        graph_copy = defaultdict(list)
        for u in self.graph:
            graph_copy[u] = self.graph[u].copy()
        
        stack = []
        cycle = []
        current_vertex = next(iter(self.graph.keys()))  # Start with any vertex
        
        while True:
            if graph_copy[current_vertex]:
                stack.append(current_vertex)
                next_vertex = graph_copy[current_vertex].pop()
                # Remove the reverse edge
                graph_copy[next_vertex].remove(current_vertex)
                current_vertex = next_vertex
            else:
                cycle.append(current_vertex)
                if not stack:
                    break
                current_vertex = stack.pop()
        
        cycle.reverse()
        return cycle