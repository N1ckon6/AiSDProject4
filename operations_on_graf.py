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
    
    def generate_hamiltonian_graph(self, num_nodes, saturation, notham):
        self.num_nodes = num_nodes
        self.saturation = saturation
        self.mode = "hamilton"
        if notham == False and num_nodes <= 10:
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
        self.generate_hamiltonian_graph(num_nodes, 50, True)
        
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
    
    def _hamiltonian_cycle_util(self, current_vertex, path, visited, start_node):
        visited[current_vertex] = True
        path.append(current_vertex)

        # Base case: If all vertices are included in the path
        if len(path) == self.num_nodes:
            # Check if there is an edge from the last added vertex to the start_node
            if start_node in self.graph.get(current_vertex, []):
                path.append(start_node) # Complete the cycle
                return True
            else:
                # Backtrack: cannot close the cycle
                path.pop() # Remove current_vertex
                visited[current_vertex] = False
                return False

        for neighbor in sorted(self.graph.get(current_vertex, [])):
            # neighbor must be in visited keys if graph nodes are 1..num_nodes
            if not visited[neighbor]: 
                if self._hamiltonian_cycle_util(neighbor, path, visited, start_node):
                    return True # Cycle found, propagate success

        path.pop() # Remove current_vertex from path
        visited[current_vertex] = False
        return False

    def find_hamiltonian_cycle(self):
        if not self.graph:
            print("Graph is empty. Cannot find Hamiltonian cycle.")
            return None
        
        if self.num_nodes == 0:
            print("Number of nodes (self.num_nodes) is 0. Cannot determine cycle parameters.")
            return None
        
        if self.num_nodes < 1:
             print(f"Number of nodes {self.num_nodes} is too small for a cycle search.")
             return None

        path = []  # This list will store the Hamiltonian cycle if found
        visited = {i: False for i in range(1, self.num_nodes + 1)}
        start_node = -1
        if 1 in visited and 1 in self.graph: 
            start_node = 1
        else:
            valid_nodes_in_graph_keys = [n for n in sorted(self.graph.keys()) if n in visited]
            if valid_nodes_in_graph_keys:
                start_node = valid_nodes_in_graph_keys[0]
            else:
                print("No valid starting node found in the graph for Hamiltonian cycle search (e.g., graph empty or nodes outside expected range).")
                return None
        
        # Call the recursive helper. It modifies 'path'.
        if self._hamiltonian_cycle_util(start_node, path, visited, start_node):
            return path
        else:
            print(f"No Hamiltonian cycle found in the graph (search started from node {start_node}).")
            return None
    