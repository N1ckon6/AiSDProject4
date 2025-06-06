import math
import random
from collections import defaultdict

class GraphGenerator:
    def __init__(self):
        self.graph = defaultdict(list)
        self.num_nodes = 0
        # self.saturation = 0 # Not stored as a persistent attribute after generation
        # self.mode = "" # Not stored as a persistent attribute after generation
    
    def add_edge(self, u, v):
        if u <= 0 or v <= 0: # Basic check for valid node IDs
            # print(f"Warning: Attempting to add edge with non-positive node ID ({u}, {v})")
            return
        if v not in self.graph[u]:
            self.graph[u].append(v)
        if u not in self.graph[v]:
            self.graph[v].append(u)
    
    def generate_hamiltonian_graph(self, num_nodes_input, saturation_percent, notham_flag):
        # Reset graph state for a new generation
        self.graph = defaultdict(list)
        self.num_nodes = 0 

        if not notham_flag and num_nodes_input <= 10:
            print("Error: Number of nodes must be greater than 10 for Hamiltonian graph generation when notham_flag is False.")
            return
        
        if num_nodes_input <= 0:
            print("Error: Number of nodes must be positive.")
            return
        
        self.num_nodes = num_nodes_input # Set the number of nodes for this graph instance

        nodes = list(range(1, self.num_nodes + 1))
        random.shuffle(nodes)
        
        # 1. Create a Hamiltonian cycle
        current_edges_count = 0
        if self.num_nodes > 0: # Only add cycle if there are nodes
            for i in range(self.num_nodes):
                # For n=1, (nodes[0] % nodes[0]) would be an edge to itself, which is fine for defaultdict.
                # For n=0, this loop doesn't run.
                u_node = nodes[i]
                v_node = nodes[(i + 1) % self.num_nodes]
                self.add_edge(u_node, v_node)
            # In an undirected graph, adding (a,b) and (b,a) counts as 1 edge.
            # The Hamiltonian cycle has num_nodes edges.
            current_edges_count = self.num_nodes if self.num_nodes > 1 else 0
            if self.num_nodes == 1: # A single node has 0 edges.
                current_edges_count = 0


        # Calculate target number of edges
        if self.num_nodes <= 1:
            max_possible_edges = 0
        else:
            max_possible_edges = self.num_nodes * (self.num_nodes - 1) // 2
        
        target_edges = int(max_possible_edges * saturation_percent / 100)
        
        # Ensure target_edges is reasonable
        target_edges = max(target_edges, current_edges_count)
        target_edges = min(target_edges, max_possible_edges)

        # 2. Add additional edges to meet saturation_percent
        # Collect all edges already present from the Hamiltonian cycle
        existing_edges_set = set()
        if self.num_nodes > 0:
            for i in range(self.num_nodes):
                u_node_s, v_node_s = sorted((nodes[i], nodes[(i + 1) % self.num_nodes]))
                if u_node_s != v_node_s : # Avoid self-loop for n=1 in set for counting
                     existing_edges_set.add((u_node_s, v_node_s))
        
        # Collect all possible new edges (not in the cycle yet)
        possible_new_edges = []
        if self.num_nodes > 1:
            for r_u in range(1, self.num_nodes + 1):
                for r_v in range(r_u + 1, self.num_nodes + 1):
                    if tuple(sorted((r_u, r_v))) not in existing_edges_set:
                        possible_new_edges.append((r_u, r_v))
        
        random.shuffle(possible_new_edges)
        
        edges_to_add_needed = target_edges - current_edges_count
        added_extra_count = 0
        
        for edge_u, edge_v in possible_new_edges:
            if added_extra_count >= edges_to_add_needed:
                break
            self.add_edge(edge_u, edge_v)
            # current_edges_count += 1 # This count was already based on the set.
            added_extra_count += 1
        
        # Final setup for single node graph
        if self.num_nodes == 1 and 1 not in self.graph:
            self.graph[1] = [] # Ensure node 1 exists as a key

    def generate_non_hamiltonian_graph(self, num_nodes_input):
        self.graph = defaultdict(list) # Reset
        self.num_nodes = 0

        if num_nodes_input <= 0:
            print("Error: Number of nodes must be a positive integer for non-Hamiltonian graph.")
            return

        # Generate a Hamiltonian graph first (with 50% saturation, notham_flag=True)
        # notham_flag=True bypasses the >10 nodes restriction in generate_hamiltonian_graph
        self.generate_hamiltonian_graph(num_nodes_input, 70, True)

        if not self.graph and num_nodes_input > 0:
            print(f"Could not generate base Hamiltonian graph for n={num_nodes_input} to make non-Hamiltonian.")
            self.num_nodes = 0 # Indicate failure
            return
        # self.num_nodes is now set by generate_hamiltonian_graph

        if self.num_nodes > 1: # Only isolate if there's more than one node
            node_to_isolate = random.randint(1, self.num_nodes)
            
            if node_to_isolate in self.graph:
                # Remove edges from other nodes to the isolated node
                for neighbor in list(self.graph[node_to_isolate]): # Iterate over a copy
                    if node_to_isolate in self.graph[neighbor]:
                        self.graph[neighbor].remove(node_to_isolate)
                # Clear the isolated node's own adjacency list
                self.graph[node_to_isolate] = []
            # Ensure the node key exists even if isolated
            elif 1 <= node_to_isolate <= self.num_nodes :
                 self.graph[node_to_isolate] = []


        elif self.num_nodes == 1:
            # For n=1, it's already non-Hamiltonian. {1: []}
            if 1 not in self.graph: # Should be set by generate_hamiltonian_graph
                self.graph[1] = []
    
    def print_graph(self):
        if not self.graph and self.num_nodes > 0: # Potentially graph with nodes but no edges
             print(f"\nGraph with {self.num_nodes} nodes and no edges (or only isolated nodes).")
             for node in range(1, self.num_nodes + 1):
                 print(f"{node}: []")
             print("\nNode degrees:")
             for node in range(1, self.num_nodes + 1):
                 print(f"Node {node}: 0")
             return
        if not self.graph:
            print("Graph is empty.")
            return
                
        print("\nAdjacency list:")
        # Ensure all nodes from 1 to num_nodes are printed, even if isolated
        all_nodes_to_print = set(self.graph.keys())
        if self.num_nodes > 0:
            all_nodes_to_print.update(range(1,self.num_nodes+1))

        for node in sorted(list(all_nodes_to_print)):
            print(f"{node}: {sorted(self.graph.get(node, []))}")
        
        print("\nNode degrees:")
        for node in sorted(list(all_nodes_to_print)):
            print(f"Node {node}: {len(self.graph.get(node, []))}")

    def is_eulerian(self):
        if not self.graph:
            return False # An empty graph might be considered Eulerian by some defs, but usually needs connected non-empty.
                         # For cycle finding, non-empty is implied.
        if self.num_nodes == 0: return False

        for node_key in self.graph: # Check degrees of nodes present in graph
            if len(self.graph[node_key]) % 2 != 0:
                return False
        # Also check nodes that might be in range 1..num_nodes but isolated (degree 0 - even)
        for i in range(1, self.num_nodes + 1):
            if i not in self.graph and 0 % 2 != 0: # Degree 0 is even
                 return False # This condition is never true, effectively means isolated nodes are fine.
        return True # All present nodes have even degree
    
    def find_eulerian_cycle(self):
        if not self.is_eulerian():
            print("Graph is not Eulerian (not all vertices have even degree or graph is unsuitable).")
            return None
        
        if not self.graph: # No edges, no cycle
            print("Graph is empty or has no edges, no Eulerian cycle.")
            return None

        # Ensure graph is connected (Hierholzer assumes this for a single cycle)
        # For simplicity, this check is omitted here but is important for strict Eulerianess.
        # The algorithm will find a cycle in the connected component of the start node.

        graph_copy = defaultdict(list)
        start_node = -1
        for u_node in self.graph:
            if self.graph[u_node]: # Find a node with edges to start
                start_node = u_node
            graph_copy[u_node] = self.graph[u_node].copy()
        
        if start_node == -1: # No edges in the graph
            print("Graph has no edges, no Eulerian cycle.")
            return None
            
        stack = []
        cycle = []
        current_vertex = start_node
        
        while True:
            if graph_copy[current_vertex]:
                stack.append(current_vertex)
                next_vertex = graph_copy[current_vertex].pop()
                # Remove the reverse edge as it's an undirected graph
                if current_vertex in graph_copy[next_vertex]: # Check if reverse edge exists
                    graph_copy[next_vertex].remove(current_vertex)
                else:
                    # This case should ideally not happen in a consistent undirected graph representation
                    # where add_edge adds symmetrically.
                    # print(f"Warning: Edge {current_vertex}-{next_vertex} found, but not {next_vertex}-{current_vertex} in copy during Euler.")
                    pass
                current_vertex = next_vertex
            else:
                cycle.append(current_vertex)
                if not stack:
                    break
                current_vertex = stack.pop()
        
        cycle.reverse()
        if not cycle or cycle[0] != cycle[-1]: # Basic check for cycle property
            # This might happen if graph was not truly Eulerian (e.g. disconnected components with edges)
            # print("Hierholzer's algorithm did not produce a valid cycle for the given graph component.") # More detailed error.
            return None # Or return the path found. For strict cycle, return None.
        return cycle
    
    def _hamiltonian_cycle_util(self, current_vertex, path, visited, start_node):
        visited[current_vertex] = True
        path.append(current_vertex)

        if len(path) == self.num_nodes:
            if start_node in self.graph.get(current_vertex, []):
                path.append(start_node) 
                return True
            else:
                path.pop() 
                visited[current_vertex] = False
                return False

        # Iterate over sorted neighbors for deterministic behavior (optional but good for testing)
        for neighbor in sorted(self.graph.get(current_vertex, [])):
            if neighbor in visited and not visited[neighbor]: # Ensure neighbor is a valid node key
                if self._hamiltonian_cycle_util(neighbor, path, visited, start_node):
                    return True 
            elif neighbor not in visited:
                # This case implies neighbor is outside the 1..num_nodes range if visited was initialized for that range.
                # Or num_nodes was not set correctly.
                # For safety, only proceed if neighbor is in visited's keys.
                # print(f"Warning: Neighbor {neighbor} of {current_vertex} not in visited keys during Hamiltonian search.")
                pass


        path.pop() 
        visited[current_vertex] = False
        return False

    def find_hamiltonian_cycle(self):
        if not self.graph and self.num_nodes > 0: # Graph with nodes but no edges
            print(f"Graph has {self.num_nodes} nodes but no edges. Cannot find Hamiltonian cycle.")
            return None
        if not self.graph:
            print("Graph is empty. Cannot find Hamiltonian cycle.")
            return None
        if self.num_nodes == 0:
            print("Number of nodes (self.num_nodes) is 0. Cannot determine cycle parameters.")
            return None
        if self.num_nodes < 1: # Pathological cases
             print(f"Number of nodes {self.num_nodes} is too small for a typical cycle search.")
             return None
        # Standard Hamiltonian cycle definition often requires N >= 3.
        # This algorithm might find A-B-A for N=2.

        path = [] 
        visited = {i: False for i in range(1, self.num_nodes + 1)}
        
        # Try to find a valid starting node that is part of the graph and within the expected node range
        start_node = -1
        # Prefer to start from node 1 if it exists and has edges, or just exists.
        potential_starts = [n for n in range(1, self.num_nodes + 1) if n in self.graph]
        if not potential_starts: # No nodes from 1..num_nodes are in graph.keys() (e.g. empty graph)
            # Or if self.graph contains nodes outside 1..num_nodes range, which shouldn't happen with current generation
            print("No valid starting node found (e.g., graph empty or nodes outside expected range 1..num_nodes).")
            return None

        # Pick the first available node from the expected range as a starting point.
        # Sorting potential_starts makes the choice deterministic if multiple options exist.
        start_node = sorted(potential_starts)[0]
        
        if self._hamiltonian_cycle_util(start_node, path, visited, start_node):
            return path
        else:
            print(f"No Hamiltonian cycle found in the graph (search started from node {start_node}).")
            return None
    
    def export_to_tikz(self, filename=None):
        if self.num_nodes == 0:
            if filename:
                with open(filename, 'w') as f:
                    f.write("% Graph is empty or not generated (0 nodes).\n\\begin{tikzpicture}\n\\node at (0,0) {Empty Graph (0 nodes)};\n\\end{tikzpicture}")
                print(f"Empty graph TikZ placeholder saved to {filename}")
            return "% Graph is empty (0 nodes).\n\\begin{tikzpicture}\n\\node at (0,0) {Empty Graph (0 nodes)};\n\\end{tikzpicture}"

        angle_step = 360 / self.num_nodes if self.num_nodes > 0 else 0
        node_positions = {}
        for i in range(1, self.num_nodes + 1): # Assumes nodes are 1 to num_nodes
            angle = (i - 1) * angle_step
            # Avoid exact overlap for small num_nodes if radius is tiny
            radius = max(0.5, 0.5 * self.num_nodes / (math.pi)) # Basic scaling for radius
            radius = min(radius, 5) # Cap radius
            if self.num_nodes == 1: radius = 0 # Place single node at origin

            x = round(radius * math.cos(math.radians(angle)), 2)
            y = round(radius * math.sin(math.radians(angle)), 2)
            node_positions[i] = (x, y)
        
        tikz_code = "\\begin{tikzpicture}[scale=1.0, every node/.style={circle, draw, fill=white!90!blue, minimum size=8pt, inner sep=1pt}]\n"
        
        drawn_edges = set()
        # Iterate through graph keys, but ensure positions are available from node_positions
        sorted_graph_nodes = sorted(self.graph.keys())

        for u_node in sorted_graph_nodes:
            if u_node not in node_positions: continue # Skip drawing edges for nodes not in 1..num_nodes range
            for v_node in sorted(self.graph[u_node]):
                if v_node not in node_positions: continue

                # Use tuple(sorted(...)) for undirected edges in drawn_edges set
                edge_pair = tuple(sorted((u_node, v_node)))
                if edge_pair not in drawn_edges:
                    x1, y1 = node_positions[u_node]
                    x2, y2 = node_positions[v_node]
                    tikz_code += f"    \\draw ({x1:.2f},{y1:.2f}) -- ({x2:.2f},{y2:.2f});\n"
                    drawn_edges.add(edge_pair)
        
        # Draw nodes based on node_positions (1 to num_nodes)
        for node_id, (x, y) in node_positions.items():
            # Only draw if node_id is actually part of the graph structure (has key or is target node count)
            # This ensures even isolated nodes within 1..num_nodes are drawn.
             tikz_code += f"    \\node at ({x:.2f},{y:.2f}) ({node_id}) {{{node_id}}};\n"
    
        tikz_code += "\\end{tikzpicture}"
        
        if filename:
            with open(filename, 'w') as f:
                f.write(tikz_code)
            print(f"TikZ code saved to {filename}")
        return tikz_code