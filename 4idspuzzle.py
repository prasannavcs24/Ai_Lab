class EightPuzzle:
    def __init__(self, start_state, goal_state=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        self.start_state = start_state
        self.goal_state = goal_state

    def get_neighbors(self, state):
        """Generates valid successor states by moving the blank tile (0)."""
        neighbors = []
        zero_idx = state.index(0)
        row, col = divmod(zero_idx, 3)

        # Possible moves: (delta_row, delta_col)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 3 and 0 <= c < 3:
                new_zero_idx = r * 3 + c
                state_list = list(state)
                # Swap blank tile with adjacent tile
                state_list[zero_idx], state_list[new_zero_idx] = state_list[new_zero_idx], state_list[zero_idx]
                neighbors.append(tuple(state_list))

        return neighbors


def depth_limited_search(puzzle, current_state, limit, path, visited_in_path):
    """Depth-Limited Search for 8-Puzzle with path cycle checking."""
    if current_state == puzzle.goal_state:
        return True, path

    if limit <= 0:
        return False, None

    for neighbor in puzzle.get_neighbors(current_state):
        # Prevent cycles along the current branch
        if neighbor not in visited_in_path:
            visited_in_path.add(neighbor)
            path.append(neighbor)

            found, result_path = depth_limited_search(puzzle, neighbor, limit - 1, path, visited_in_path)
            if found:
                return True, result_path

            # Backtrack
            path.pop()
            visited_in_path.remove(neighbor)

    return False, None


def solve_8_puzzle_ids(start_state, max_depth=30):
    puzzle = EightPuzzle(start_state)
    
    for depth in range(max_depth + 1):
        path = [start_state]
        visited_in_path = {start_state}
        
        found, result_path = depth_limited_search(puzzle, start_state, depth, path, visited_in_path)
        
        if found:
            print(f"Goal reached at depth {depth} (total moves: {len(result_path) - 1})!")
            return result_path

    print(f"No solution found within max depth {max_depth}.")
    return None


def print_board(state):
    """Helper to pretty-print the 3x3 board."""
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


# --- Example Usage ---
if __name__ == "__main__":
    # 0 represents the empty space
    # Simple start state (3 moves from goal)
    start = (1, 2, 3, 4, 5, 0, 7, 8, 6)

    solution_path = solve_8_puzzle_ids(start, max_depth=10)

    if solution_path:
        print("Solution Steps:")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            print_board(state)