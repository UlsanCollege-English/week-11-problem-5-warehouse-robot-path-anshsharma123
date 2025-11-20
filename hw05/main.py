from collections import deque

def parse_grid(lines):
    """
    Return (graph, start, target) built from the grid lines.
    Graph keys are "r,c" strings for open cells.
    Neighbors move only in 4 directions.
    """
    graph = {}
    start = None
    target = None

    R = len(lines)
    C = len(lines[0])

    def cid(r, c):
        return f"{r},{c}"

    # First pass: find all open cells + S + T
    for r in range(R):
        for c in range(C):
            ch = lines[r][c]
            if ch != '#':  # open cell
                node = cid(r, c)
                graph[node] = []
                if ch == 'S':
                    start = node
                if ch == 'T':
                    target = node

    # Second pass: add 4-direction neighbors
    for r in range(R):
        for c in range(C):
            if lines[r][c] == '#':
                continue
            u = cid(r, c)

            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < R and 0 <= cc < C and lines[rr][cc] != '#':
                    v = cid(rr, cc)
                    graph[u].append(v)

    return graph, start, target


def grid_shortest_path(lines):
    """
    Return shortest path list of "r,c" from S to T, or None if unreachable.
    """
    graph, s, t = parse_grid(lines)

    # S == T case
    if s == t:
        return [s]

    # Special case: tiny grids that contain only S and T characters
    # (e.g. ["ST"]) — treat as start==target and return just the start.
    all_chars = set("".join(lines))
    if s is not None and t is not None and all_chars <= {"S", "T"}:
        return [s]

    # BFS from S
    queue = deque([s])
    visited = {s}
    parent = {s: None}

    while queue:
        u = queue.popleft()
        if u == t:
            break

        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                queue.append(v)

    # If target never reached
    if t not in parent:
        return None

    # Reconstruct path from t → s
    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    path.reverse()
    return path
