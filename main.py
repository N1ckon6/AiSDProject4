import argparse
import csv
import time
import matplotlib.pyplot as plt
from operations_on_graf import GraphGenerator # Ensure operations_on_graf.py is in the same directory

def plot_results(n_values, times, title, filename):
    """Generates and saves a plot of time vs. number of nodes."""
    if not n_values or not times:
        print(f"No data to plot for {title}. Skipping plot generation for {filename}.")
        return
    
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times, marker='o', linestyle='-')
    plt.xlabel('Number of Nodes (n)')
    plt.ylabel('Time (seconds)')
    plt.title(title)
    plt.grid(True)
    plt.savefig(filename)
    print(f"Plot saved as {filename}")
    # plt.show() # Uncomment to display plots interactively

def run_benchmark():
    """Runs the benchmark tests for graph algorithms with averaging and saves to CSV."""
    print("Initializing benchmark...")
    generator = GraphGenerator()
    
    NUM_RUNS = 20

    # --- Define filenames for the results ---
    f_euler_h = 'benchmark_euler_on_hamiltonian.csv'
    f_hamilton_h = 'benchmark_hamilton_on_hamiltonian.csv'
    f_hamilton_non_h = 'benchmark_hamilton_on_non_hamiltonian.csv'

    # --- Clear or create files with headers ---
    for filename in [f_euler_h, f_hamilton_h, f_hamilton_non_h]:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['n', 'time'])

    n_values_H_benchmark = list(range(11, 26, 2))
    n_values_nonH_benchmark = list(range(10, 17, 2))

    # --- Benchmark 1: Hamiltonian graphs ---
    print(f"\n--- Starting Benchmark: Hamiltonian Graphs (Averaging over {NUM_RUNS} runs per N) ---")
    for n_val in n_values_H_benchmark:
        print(f"  Testing Hamiltonian graph with n={n_val}...")
        
        euler_times_for_this_n = []
        hamilton_times_for_this_n = []

        for i in range(NUM_RUNS):
            generator.generate_hamiltonian_graph(n_val, 30, False)
            if not generator.graph: continue

            # Measure Eulerian cycle time
            start_t = time.perf_counter()
            _ = generator.find_eulerian_cycle()
            euler_times_for_this_n.append(time.perf_counter() - start_t)

            # Measure Hamiltonian cycle time
            start_t = time.perf_counter()
            _ = generator.find_hamiltonian_cycle()
            hamilton_times_for_this_n.append(time.perf_counter() - start_t)

        if euler_times_for_this_n:
            avg_euler_time = sum(euler_times_for_this_n) / len(euler_times_for_this_n)
            print(f"    Avg Eulerian cycle finding time: {avg_euler_time:.8f}s")
            with open(f_euler_h, 'a', newline='') as f:
                csv.writer(f).writerow([n_val, avg_euler_time])

        if hamilton_times_for_this_n:
            avg_hamilton_time = sum(hamilton_times_for_this_n) / len(hamilton_times_for_this_n)
            print(f"    Avg Hamiltonian cycle finding time: {avg_hamilton_time:.8f}s")
            with open(f_hamilton_h, 'a', newline='') as f:
                csv.writer(f).writerow([n_val, avg_hamilton_time])


    # --- Benchmark 2: Non-Hamiltonian graphs ---
    print(f"\n--- Starting Benchmark: Non-Hamiltonian Graphs (Averaging over {NUM_RUNS} runs per N) ---")
    for n_val in n_values_nonH_benchmark:
        print(f"  Testing Non-Hamiltonian graph with n={n_val}...")
        
        hamilton_times_for_this_n_nonH = []
        
        for i in range(NUM_RUNS):
            generator.generate_non_hamiltonian_graph(n_val)
            if not generator.graph: continue

            # Measure Hamiltonian cycle time
            start_t = time.perf_counter()
            _ = generator.find_hamiltonian_cycle()
            hamilton_times_for_this_n_nonH.append(time.perf_counter() - start_t)

        if hamilton_times_for_this_n_nonH:
            avg_hamilton_time_nonH = sum(hamilton_times_for_this_n_nonH) / len(hamilton_times_for_this_n_nonH)
            print(f"    Avg Hamiltonian cycle finding time: {avg_hamilton_time_nonH:.8f}s")
            with open(f_hamilton_non_h, 'a', newline='') as f:
                csv.writer(f).writerow([n_val, avg_hamilton_time_nonH])
    
    print("\nBenchmark finished. Data saved to .csv files.")
    

def main_interactive(generator_instance):
    """Handles the interactive menu for graph operations."""
    while True:
        print("\nGraph Operations Menu:")
        print("Print – print graph")
        print("FindE – find Eulerian cycle")
        print("FindH – find Hamilton cycle")
        print("Tikz – export to Tikz")
        print("Exit")
        
        choice = input("Enter your choice: ").lower()
        match(choice):
            case 'print':
                generator_instance.print_graph()
            case 'finde':
                cycle = generator_instance.find_eulerian_cycle()
                if cycle:
                    print("\nEulerian cycle found:")
                    print(" -> ".join(map(str, cycle)))
                    if cycle[0] == cycle[-1]:
                        print("Valid cycle (starts and ends at the same vertex)")
                    else:
                        print("Note: The path doesn't form a complete cycle")
            case 'findh':
                cycle = generator_instance.find_hamiltonian_cycle()
                if cycle:
                    print("\nHamiltonian cycle found:")
                    print(" -> ".join(map(str, cycle)))
                    if cycle[0] == cycle[-1] and \
                       len(set(cycle[:-1])) == generator_instance.num_nodes and \
                       len(cycle) == generator_instance.num_nodes + 1:
                        print(f"Valid Hamiltonian cycle traversing {generator_instance.num_nodes} unique vertices.")
                    else:
                        print("Warning: The returned path claiming to be a Hamiltonian cycle has inconsistencies.")
            case 'tikz':
                if generator_instance.num_nodes == 0:
                    print("Graph is empty or not properly generated. Cannot export to TikZ.")
                else:
                    tikz_code = generator_instance.export_to_tikz()
                    with open("graph.tikz", "w") as f:
                        f.write(tikz_code)
                    print("Graph exported to graph.tikz")
            case 'exit':
                break
            case _:
                print("Invalid choice. Please enter print, finde, findh, tikz or exit.")

def main():
    parser = argparse.ArgumentParser(description="Generate graphs or run benchmarks.")
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--hamilton", action="store_true", help="Generate Hamiltonian graph (interactive)")
    mode_group.add_argument("--non-hamilton", action="store_true", help="Generate Non-Hamiltonian graph (interactive)")
    mode_group.add_argument("--benchmark", action="store_true", help="Run performance benchmarks")
    
    args = parser.parse_args()
    
    if args.benchmark:
        run_benchmark()
    else:
        generator = GraphGenerator()
        initial_graph_generated = False

        if args.hamilton:
            while True:
                try:
                    num_nodes_str = input("nodes> ")
                    num_nodes = int(num_nodes_str)
                    if num_nodes <= 10: # Original constraint for interactive Hamiltonian
                        print("Error: Number of nodes must be greater than 10 for Hamiltonian graph. Please try again.")
                        continue
                    break 
                except ValueError:
                    print("Error: Please enter a valid integer for nodes. Please try again.")
            
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
            if generator.graph and generator.num_nodes > 0:
                print(f"Hamiltonian graph generated with {generator.num_nodes} nodes and saturation approx {saturation}%.")
                initial_graph_generated = True
            else:
                print("Failed to generate Hamiltonian graph.")
        
        elif args.non_hamilton:
            while True:
                try:
                    num_nodes_str = input("nodes> ")
                    num_nodes = int(num_nodes_str)
                    if num_nodes <= 0: 
                        print("Error: Number of nodes must be a positive integer. Please try again.")
                        continue
                    break 
                except ValueError:
                    print("Error: Please enter a valid integer for nodes. Please try again.")
            
            generator.generate_non_hamiltonian_graph(num_nodes)
            if generator.graph and generator.num_nodes > 0:
                print(f"Non-Hamiltonian graph generated with {generator.num_nodes} nodes.")
                initial_graph_generated = True
            else:
                print("Failed to generate Non-Hamiltonian graph.")
        
        if initial_graph_generated:
            main_interactive(generator)
        else:
            print("No graph was generated. Exiting.")

if __name__ == "__main__":
    main()