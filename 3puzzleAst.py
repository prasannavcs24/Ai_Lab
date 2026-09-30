import heapq

GOAL_STATE = (1, 2, 3, 
              4, 5, 6, 
              7, 8, 0)

def manhattan_distance(state):
    """Calculates the total Manhattan distance of all tiles from target positions."""
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            # Target position for tile `t` is `t - 1`
            target_idx = tile - 1
            current_row, current_col = divmod(i, 3)
            target_row, target_col = divmod(target_idx, 3)
            distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance

def is_solvable(state):
    """An 8-puzzle state is solvable if the number of inversions is even."""
    inversions = 0
    tiles = [tile for tile in state if tile != 0]
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0

def get_neighbors(state):
    """Generates all valid successor states by sliding tiles into the blank space (0)."""
    neighbors = []
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 3)
    
    # Moves: (row_offset, col_offset)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_idx = new_row * 3 + new_col
            # Swap blank space with neighbor
            state_list = list(state)
            state_list[zero_idx], state_list[new_zero_idx] = state_list[new_zero_idx], state_list[zero_idx]
            neighbors.append(tuple(state_list))
            
    return neighbors

def solve_8_puzzle(initial_state):
    """Solves the 8-puzzle problem using A* Search Algorithm."""
    if not is_solvable(initial_state):
        return None
    
    # Priority Queue store format: (f_score, g_score, current_state, path)
    initial_h = manhattan_distance(initial_state)
    frontier = [(initial_h, 0, initial_state, [initial_state])]
    visited = set()

    while frontier:
        f, g, current, path = heapq.heappop(frontier)

        if current == GOAL_STATE:
            return path

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                new_g = g + 1
                new_h = manhattan_distance(neighbor)
                heapq.heappush(frontier, (new_g + new_h, new_g, neighbor, path + [neighbor]))

    return None

def print_board(state):
    """Prints a 3x3 board cleanly."""
    for i in range(0, 9, 3):
        row = ["_" if x == 0 else str(x) for x in state[i:i+3]]
        print(" ".join(row))
    print()

# Example Usage
if __name__ == "__main__":
    start_state = (5, 7, 6, 
                   4, 0, 2, 
                   3, 1, 8)
    
    solution_path = solve_8_puzzle(start_state)
    
    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} moves:\n")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            print_board(state)
    else:
        print("This board configuration is unsolvable.")