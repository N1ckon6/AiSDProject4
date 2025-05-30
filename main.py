import argparse

from operations_on_graf import GraphGenerator


def main():
    parser = argparse.ArgumentParser(description="Generate Hamiltonian or Non-Hamiltonian graphs")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--hamilton", action="store_true", help="Generate Hamiltonian graph")
    group.add_argument("--non-hamilton", action="store_true", help="Generate Non-Hamiltonian graph")
    
    args = parser.parse_args()
    
    generator = GraphGenerator()
    
    if args.hamilton:
        while True:
            try:
                num_nodes_str = input("nodes> ")
                num_nodes = int(num_nodes_str)
                if num_nodes <= 10:
                    print("Error: Number of nodes must be greater than 10 for Hamiltonian graph. Please try again.")
                    continue

                while True:
                    try:
                        saturation_str = input("saturation> ")
                        saturation = int(saturation_str)
                        if saturation not in [30, 70]:
                            print("Error: Saturation must be either 30% or 70% for Hamiltonian graph. Please try again.")
                            continue
                        break
                    except ValueError:
                        print("Error: Please enter a valid integer for saturation. Please try again.")
                        
                generator.generate_hamiltonian_graph(num_nodes, saturation, False)
                break 
            except ValueError:
                print("Error: Please enter valid integers for nodes and saturation. Please try again.")
    else: 
        while True:
            try:
                num_nodes_str = input("nodes> ")
                num_nodes = int(num_nodes_str)
                if num_nodes <= 0: 
                    print("Error: Number of nodes must be a positive integer. Please try again.")
                    continue 

                generator.generate_non_hamiltonian_graph(num_nodes)
                break
            except ValueError:
                print("Error: Please enter a valid integer for nodes. Please try again.")
    
    # Interactive menu for operations
    while True:
        print("\nGraph Operations Menu:")
        print("1. Print graph")
        print("2. Find Eulerian cycle")
        print("3. Find Hamilton cycle")
        print("4. Export to Tikz")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        match(choice):
            case '1':
                 generator.print_graph()
            case '2':
                cycle = generator.find_eulerian_cycle()
                if cycle:
                    print("\nEulerian cycle found:")
                    print(" -> ".join(map(str, cycle)))
                    # Check if it's actually a cycle
                    if cycle[0] == cycle[-1]:
                        print("Valid cycle (starts and ends at the same vertex)")
                    else:
                        print("Note: The path doesn't form a complete cycle")
            case '3':
                cycle = generator.find_hamiltonian_cycle()
                if cycle:
                    print("\nHamiltonian cycle found:")
                    print(" -> ".join(map(str, cycle)))
                    # Basic validation output (algorithm ensures properties)
                    if cycle[0] == cycle[-1] and len(set(cycle[:-1])) == generator.num_nodes and len(cycle) == generator.num_nodes + 1:
                         print(f"Valid Hamiltonian cycle traversing {generator.num_nodes} unique vertices.")
                    else:
                         print("Warning: The returned path claiming to be a Hamiltonian cycle has inconsistencies.")
            case '4':
                tikz_code = generator.export_to_tikz()
                with open("graph.tikz", "w") as f:
                    f.write(tikz_code)
                print("Graph exported to graph.tikz")
            case '5':
                break
            case _:
                print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()