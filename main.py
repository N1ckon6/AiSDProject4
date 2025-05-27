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
        try:
            num_nodes = int(input("nodes> "))
            if num_nodes <= 10:
                print("Error: Number of nodes must be greater than 10 for Hamiltonian graph.")
                return
            saturation = int(input("saturation> "))
            if saturation not in [30, 70]:
                print("Error: Saturation must be either 30% or 70% for Hamiltonian graph.")
                return
            generator.generate_hamiltonian_graph(num_nodes, saturation)
        except ValueError:
            print("Error: Please enter valid integers for nodes and saturation.")
            return
    else:
        try:
            num_nodes = int(input("nodes> "))
            generator.generate_non_hamiltonian_graph(num_nodes)
        except ValueError:
            print("Error: Please enter a valid integer for nodes.")
            return
    
    # Interactive menu for operations
    while True:
        print("\nGraph Operations Menu:")
        print("1. Print graph")
        print("2. Find Eulerian cycle")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            generator.print_graph()
        elif choice == '2':
            cycle = generator.find_eulerian_cycle()
            if cycle:
                print("\nEulerian cycle found:")
                print(" -> ".join(map(str, cycle)))
                # Check if it's actually a cycle
                if cycle[0] == cycle[-1]:
                    print("Valid cycle (starts and ends at the same vertex)")
                else:
                    print("Note: The path doesn't form a complete cycle")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()