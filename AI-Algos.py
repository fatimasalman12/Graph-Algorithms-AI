from collections import deque
import time
import heapq
# from memory_profiler import profile
import psutil


# Function to print the puzzle state
def print_puzzle(state):
    for row in state:
        print(" ".join(map(str, row)))
    print("-----")

# Function to find the coordinates of the blank tile
def find_blank(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == 0:
                return i, j

# Function to check if the current state is the goal state
def is_goal(state, goal_state):
    return state == goal_state

# @profile
# Function to perform BFS
def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    nodes_visited = 0

    while queue:
        current_state, path = queue.popleft()
        nodes_visited += 1

        if is_goal(current_state, goal_state):
            return path, nodes_visited

        visited.add(tuple(map(tuple, current_state)))  # Convert list of lists to tuple of tuples
        blank_i, blank_j = find_blank(current_state)

        for move_i, move_j in moves:
            new_state = [row[:] for row in current_state]  # Deep copy of the current state
            new_blank_i, new_blank_j = blank_i + move_i, blank_j + move_j
            if 0 <= new_blank_i < 3 and 0 <= new_blank_j < 3:
                new_state[blank_i][blank_j], new_state[new_blank_i][new_blank_j] = new_state[new_blank_i][new_blank_j], new_state[blank_i][blank_j]
                if tuple(map(tuple, new_state)) not in visited:
                    queue.append((new_state, path + [new_state]))

# @profile
# Function to perform DFS
def dfs(start_state, goal_state):
    stack = [(start_state, [])]
    visited = set()  # Use a set to store visited states
    nodes_visited = 0

    while stack:
        current_state, path = stack.pop()
        nodes_visited += 1

        if is_goal(current_state, goal_state):
            return path, nodes_visited

        # Convert the current state to a tuple before adding to the set
        visited.add(tuple(map(tuple, current_state)))
        blank_i, blank_j = find_blank(current_state)

        for move_i, move_j in moves:
            new_state = [row[:] for row in current_state]  # Deep copy of the current state
            new_blank_i, new_blank_j = blank_i + move_i, blank_j + move_j
            if 0 <= new_blank_i < 3 and 0 <= new_blank_j < 3:
                new_state[blank_i][blank_j], new_state[new_blank_i][new_blank_j] = new_state[new_blank_i][new_blank_j], new_state[blank_i][blank_j]
                # Convert the new state to a tuple before checking if it's visited
                if tuple(map(tuple, new_state)) not in visited:
                    stack.append((new_state, path + [new_state]))

    # If goal state not found
    return None, nodes_visited

def dfs(start_state, goal_state):
    stack = [(start_state, [])]
    visited = set()  # Use a set to store visited states
    nodes_visited = 0

    while stack:
        current_state, path = stack.pop()
        nodes_visited += 1

        if is_goal(current_state, goal_state):
            return path, nodes_visited

        # Convert the current state to a tuple before adding to the set
        visited.add(tuple(map(tuple, current_state)))
        blank_i, blank_j = find_blank(current_state)

        for move_i, move_j in moves:
            new_state = [row[:] for row in current_state]  # Deep copy of the current state
            new_blank_i, new_blank_j = blank_i + move_i, blank_j + move_j
            if 0 <= new_blank_i < 3 and 0 <= new_blank_j < 3:
                new_state[blank_i][blank_j], new_state[new_blank_i][new_blank_j] = new_state[new_blank_i][new_blank_j], new_state[blank_i][blank_j]
                # Convert the new state to a tuple before checking if it's visited
                if tuple(map(tuple, new_state)) not in visited:
                    stack.append((new_state, path + [new_state]))

    # If goal state not found
    return None, nodes_visited


# @profile
# Function to perform UCS
def ucs(start_state, goal_state):
    heap = [(0, start_state, [])]  # Priority queue to store states with their respective costs
    visited = set()
    nodes_visited = 0

    while heap:
        cost, current_state, path = heapq.heappop(heap)
        nodes_visited += 1

        if is_goal(current_state, goal_state):
            return path, nodes_visited

        # Convert the current state to a tuple before adding to the set
        visited.add(tuple(map(tuple, current_state)))
        blank_i, blank_j = find_blank(current_state)

        for move_i, move_j in moves:
            new_state = [row[:] for row in current_state]  # Deep copy of the current state
            new_blank_i, new_blank_j = blank_i + move_i, blank_j + move_j
            if 0 <= new_blank_i < 3 and 0 <= new_blank_j < 3:
                new_state[blank_i][blank_j], new_state[new_blank_i][new_blank_j] = new_state[new_blank_i][new_blank_j], new_state[blank_i][blank_j]
                if tuple(map(tuple, new_state)) not in visited:
                    # Push the new state with its cost (which is the same for all steps in UCS)
                    heapq.heappush(heap, (cost + 1, new_state, path + [new_state]))

    # If goal state not found
    return None, nodes_visited


# Function to perform DFS with limited depth
def dfs_limit(start_state, goal_state, depth_limit):
    stack = [(start_state, [])]
    nodes_visited = 0

    while stack:
        current_state, path = stack.pop()
        nodes_visited += 1

        if len(path) > depth_limit:
            continue

        if is_goal(current_state, goal_state):
            return path, nodes_visited

        blank_i, blank_j = find_blank(current_state)

        for move_i, move_j in moves:
            new_state = [row[:] for row in current_state]  # Deep copy of the current state
            new_blank_i, new_blank_j = blank_i + move_i, blank_j + move_j
            if 0 <= new_blank_i < 3 and 0 <= new_blank_j < 3:
                new_state[blank_i][blank_j], new_state[new_blank_i][new_blank_j] = new_state[new_blank_i][new_blank_j], new_state[blank_i][blank_j]
                stack.append((new_state, path + [new_state]))

    # If goal state not found within depth limit
    return None, nodes_visited
# @profile
# Function to perform Iterative Deepening Depth-First Search (IDS)
def ids(start_state, goal_state):
    depth_limit = 0
    nodes_visited_total = 0

    while True:
        # Running DFS with increasing depth limits
        path, nodes_visited = dfs_limit(start_state, goal_state, depth_limit)
        nodes_visited_total += nodes_visited

        if path is not None:
            return path, nodes_visited_total

        depth_limit += 1
# ---------------------------------------------------------------------------------------------------------------------

# Define possible movements: Up, Down, Left, Right
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Take input of start state from user
print("Enter the start state (3 rows, each row contains 3 space-separated numbers):")
start_state = []
for _ in range(3):
    row = list(map(int, input().split()))
    start_state.append(row)

goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


# -----------------------------------------------RESULTS FOR BFS--------------------------------------------------------
# Measure time
start_time = time.time()

# Running BFS algorithm
bfs_path, bfs_nodes_visited = bfs(start_state, goal_state)

# Calculate time used
time_used = time.time() - start_time

# Printing results
print("-----------------")
print("BFS Algorithm")
print("-----------------")
print("Path Cost:", len(bfs_path) - 1)
print("No of Node Visited:", bfs_nodes_visited)
print("Time Used: {:.6f} seconds".format(time_used))
print("Memory Used: {} MiB".format(psutil.Process().memory_info().rss / 1024 ** 2))
for state in bfs_path:
    print_puzzle(state)

# ---------------------------------------------RESULT PRINTING FOR DFS--------------------------------------------------

# Measure time
start_time = time.time()

# Running BFS algorithm
dfs_path, dfs_nodes_visited = dfs(start_state, goal_state)

# Calculate time used
time_used = time.time() - start_time

# Printing results
print("-----------------")
print("DFS Algorithm")
print("-----------------")
if dfs_path:
    print("Path Cost:", len(dfs_path) - 1)  # Subtracting 1 to exclude the initial state
    print("No of Node Visited:", dfs_nodes_visited)
    print("Time Used: {:.6f} seconds".format(time_used))
    print("Memory Used: {} MiB".format(psutil.Process().memory_info().rss / 1024 ** 2))
    for state in dfs_path:
        print_puzzle(state)
else:
    print("Goal state not reachable from the given start state.")

# ----------------------------------------UNIFORM COST SEARCH RESULTS HERE:---------------------------------------------

    # Measure time
start_time = time.time()

# Running UCS algorithm
ucs_path, ucs_nodes_visited = ucs(start_state, goal_state)

# Calculate time used
time_used = time.time() - start_time

# Printing results
print("-----------------")
print("UCS Algorithm")
print("-----------------")
print("Path Cost:", len(ucs_path) - 1)  # Subtracting 1 to exclude the initial state
print("No of Node Visited:", ucs_nodes_visited)
print("Time Used: {:.6f} seconds".format(time_used))
print("Memory Used: {} MiB".format(psutil.Process().memory_info().rss / 1024 ** 2))
for state in ucs_path:
    print_puzzle(state)

# -----------------------------------------------IDS RESULTS HERE:------------------------------------------------------

    # Measure time
start_time = time.time()

# Running IDS algorithm
ids_path, ids_nodes_visited = ids(start_state, goal_state)

# Calculate time used
time_used = time.time() - start_time

# Printing results
print("-----------------")
print("IDS Algorithm")
print("-----------------")
if ids_path is not None:
    print("Path Cost:", len(ids_path) - 1)  # Subtracting 1 to exclude the initial state
    print("No of Node Visited:", ids_nodes_visited)
    print("Time Used: {:.6f} seconds".format(time_used))
    print("Memory Used: {} MiB".format(psutil.Process().memory_info().rss / 1024 ** 2))
    for state in ids_path:
        print_puzzle(state)
else:
    print("Goal state not reachable within depth limit.")
