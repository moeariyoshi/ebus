import numpy as np
import heapq
import matplotlib.pyplot as plt

def get_user_inputs():
    print("Enter the importance of each location (higher is more important).")
    importance = {}
    while True:
        location = input("Enter location name (or 'done' to finish): ")
        if location.lower() == 'done':
            break
        weight = float(input(f"Enter importance weight for {location}: "))
        importance[location] = weight
    return importance

def generate_town_matrix(size):
    """Generate a sample town matrix with random locations."""
    locations = ["School", "Mall", "Hospital", "Station", "Park", "Library", "Office"]
    town = np.random.choice(locations, (size, size))
    return town

def find_best_route(town, importance):
    """Finds the best bus route based on weighted locations."""
    size = town.shape[0]
    start = (0, 0)  # Assume bus starts at (0,0)
    queue = [(0, start)]  # Min-heap with (cost, position)
    distances = {start: 0}
    prev = {}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        cost, current = heapq.heappop(queue)
        x, y = current
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size:
                loc = town[nx, ny]
                weight = -importance.get(loc, 1)  # Negative for max priority
                new_cost = cost + weight
                
                if (nx, ny) not in distances or new_cost < distances[(nx, ny)]:
                    distances[(nx, ny)] = new_cost
                    prev[(nx, ny)] = current
                    heapq.heappush(queue, (new_cost, (nx, ny)))
    
    return distances, prev

def reconstruct_path(prev, end):
    """Reconstruct the shortest path from prev mapping."""
    path = []
    while end in prev:
        path.append(end)
        end = prev[end]
    path.append((0, 0))  # Start position
    return path[::-1]

def visualize_town(town, path):
    size = town.shape[0]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xticks(range(size))
    ax.set_yticks(range(size))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    
    for i in range(size):
        for j in range(size):
            ax.text(j, size - i - 1, town[i, j], ha='center', va='center', fontsize=8, 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
    
    if path:
        x_coords, y_coords = zip(*path)
        y_coords = [size - 1 - y for y in y_coords]  # Flip y-axis for display
        ax.plot(y_coords, x_coords, marker='o', linestyle='-', color='red', markersize=8)
    
    plt.title("Town Grid with Bus Route")
    plt.show()

def main():
    size = int(input("Enter town grid size (e.g., 5 for 5x5): "))
    town = generate_town_matrix(size)
    importance = get_user_inputs()
    
    print("\nGenerated Town Layout:")
    print(town)
    
    distances, prev = find_best_route(town, importance)
    
    # Find the most important place to route to
    max_loc = max(importance, key=importance.get, default=None)
    end = None
    
    for (i, j), loc in np.ndenumerate(town):
        if loc == max_loc:
            end = (i, j)
            break
    
    if end:
        path = reconstruct_path(prev, end)
        print("\nBest Route to Most Important Location:")
        print(path)
        visualize_town(town, path)
    else:
        print("\nNo important location found.")

if __name__ == "__main__":
    main()
