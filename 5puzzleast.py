import heapq

def misplaced_tiles(state, goal):
    """Calculates number of misplaced tiles (excluding blank 0)."""
    return sum(1 for s, g in zip(state, goal) if s != 0 and s != g)

def get_neighbors(state):
    """Generates valid next states by moving the blank tile (0)."""
    neighbors = []
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 3)
    
    # Possible moves: (row_offset, col_offset)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    
    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_zero_idx = r * 3 + c
            # Create new board state
            new_state = list(state)
            new_state[zero_idx], new_state[new_zero_idx] = new_state[new_zero_idx], new_state[zero_idx]
            neighbors.append(tuple(new_state))
            
    return neighbors

def solve_8_puzzle(start_state, goal_state):
    """Solves the 8-puzzle using A* search and returns the solution path."""
    start = tuple(start_state)
    goal = tuple(goal_state)
    
    # Priority Queue stores: (f_score, h_score, current_state, path)
    # Including h_score acts as a tie-breaker (favors states closer to goal)
    initial_h = misplaced_tiles(start, goal)
    open_set = [(initial_h, initial_h, start, [start])]
    visited = {start: 0}  # state -> g_score
    
    while open_set:
        f, h, current, path = heapq.heappop(open_set)
        
        # Check if goal is reached
        if current == goal:
            return path
            
        g = len(path) - 1
        
        for neighbor in get_neighbors(current):
            tentative_g = g + 1
            
            if neighbor not in visited or tentative_g < visited[neighbor]:
                visited[neighbor] = tentative_g
                h_neighbor = misplaced_tiles(neighbor, goal)
                f_neighbor = tentative_g + h_neighbor
                heapq.heappush(open_set, (f_neighbor, h_neighbor, neighbor, path + [neighbor]))
                
    return None

def print_board(state):
    """Formats a flat 9-element tuple as a 3x3 grid."""
    for i in range(0, 9, 3):
        row = ["_" if tile == 0 else str(tile) for tile in state[i:i+3]]
        print(" " + "  ".join(row))

# --- Example Execution ---

if __name__ == "__main__":
    start_state = (2, 8, 3,
                   1, 6, 4,
                   0, 7, 5)

    goal_state  = (1, 2, 3,
                   8, 0, 4,
                   7, 6, 5)

    solution_path = solve_8_puzzle(start_state, goal_state)

    print("=== 8-PUZZLE A* SOLUTION STEPS ===")
    for step, state in enumerate(solution_path):
        g = step
        h = misplaced_tiles(state, goal_state)
        f = g + h
        
        print(f"\n--- Step {step} --- (g = {g}, h = {h}, f = {f})")
        print_board(state)

    print(f"\nGoal reached in {len(solution_path) - 1} moves!")