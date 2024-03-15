import sys
import numpy as np

def read_input_file(file_path):
    """
    Read the input file and extract information about the resource allocation graph.
    Return number of processes, number of resources, units of each resource type, and adjacency matrix.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Extract number of processes and resources
        num_processes = None
        num_resources = None
        resource_units = None
        adjacency_matrix = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('%') or len(line) == 0:
                continue  # Skip comments and blank lines
            elif line.startswith('num_processes'):
                num_processes = int(line.split('=')[1])
            elif line.startswith('num_resources'):
                num_resources = int(line.split('=')[1])
            elif resource_units is None:
                resource_units = list(map(int, line.split(',')))
            else:
                adjacency_matrix.append(list(map(int, line.split(','))))

    return num_processes, num_resources, resource_units, np.array(adjacency_matrix)

def convert_to_graph(adjacency_matrix):
    """
    Convert the adjacency matrix to a graph.
    Returns a dictionary representation of the graph.
    """
    graph = {}
    num_nodes = len(adjacency_matrix)
    for i in range(num_nodes):
        allocated_resources = [j for j, val in enumerate(adjacency_matrix[i]) if val > 0]
        graph[i] = allocated_resources
    return graph

def graph_reduction(adjacency_matrix, resource_units):
    """
    Perform graph reduction to check for deadlock.
    Returns True if deadlock is detected, False otherwise.
    """
    graph = convert_to_graph(adjacency_matrix)
    num_processes = len(graph)
    
    # Ensure resource_units list has enough elements
    while len(resource_units) < num_processes:
        resource_units.append(0)
    
    while True:
        node_removed = False
        
        for i in range(num_processes):
            if sum(adjacency_matrix[i]) < resource_units[i]:  # Process can be executed
                node_removed = True
                # Remove the process and associated edges
                adjacency_matrix[i] = np.zeros_like(adjacency_matrix[i])
                for j in range(num_processes):
                    adjacency_matrix[j][i] = 0
                resource_units += adjacency_matrix[:, i]
        
        if not node_removed:
            break
    
    return not np.any(adjacency_matrix)

def main():
    if len(sys.argv) != 2:
        print("Usage: python deadlock_detection.py <input_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    num_processes, num_resources, resource_units, adjacency_matrix = read_input_file(file_path)
    
    deadlock_detected = graph_reduction(adjacency_matrix, resource_units)
    
    if deadlock_detected:
        print("Deadlock Detected!")
    else:
        print("No Deadlock Detected.")

if __name__ == "__main__":
    main()

