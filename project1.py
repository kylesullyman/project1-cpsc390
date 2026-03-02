#!CAUSION: NO OTHER IMPORTS ARE ALLOWED!
import math


#NOTE: You must use the Node class below to define your nodes
class Node:
    def __init__(self, state, parent=None, action=None, g=0.0, h=0.0, w=1.0):
        self.state = state     # (x, y)
        self.parent = parent   # Parent Node object
        self.action = action   # e.g., "U", "UR"
        self.g = float(g)      # Path-cost from start to this node
        self.h = float(h)      # Heuristic estimate to goal
        self.w = float(w)      # When w>1.0, A* -> Weighted A*
        self.f = self.g + self.w * self.h # total estimated cost

        # evaluation cost for A*
        self.evalCost = self.g + self.h

class ReachedSet:
    """
    Lookup table for tracking already-explored states in search algorithms.

    Internally uses a dictionary keyed by state for O(1) average-case
    add, lookup, and update operations — without using Python's built-in set.

    Structure:
        _table: dict { state (tuple) -> Node }
    """

    def __init__(self):
        self._table = {}      # { state: Node }
        self._keys = []       # insertion-ordered list of state keys

    def add(self, node):
        """Mark a state as reached, storing its node."""
        if node.state not in self._table:
            self._keys.append(node.state)
        self._table[node.state] = node

    def contains(self, state):
        """Return True if state has already been reached."""
        return state in self._table

    def get(self, state):
        """Return the Node stored for the given state, or None."""
        return self._table.get(state, None)

    def get_cost(self, state):
        """Return the g-cost of the reached node for state, or infinity."""
        node = self._table.get(state, None)
        return node.g if node is not None else float('inf')

    def update(self, node):
        """Replace the stored node for a state (e.g. cheaper path found)."""
        self._table[node.state] = node

    def remove(self, state):
        """Remove a state from the reached set (for re-expansion)."""
        if state in self._table:
            del self._table[state]
            self._keys = [k for k in self._keys if k != state]

    def states(self):
        """Return a list of all reached states in insertion order."""
        return list(self._keys)

    def __len__(self):
        return len(self._table)

    def __repr__(self):
        return f"ReachedSet({list(self._table.keys())})"


class Frontier:
    # priority queue format
    # 0th index as head of queue (lowest f)
    def __init__(self):
        self.queue = []

    def push(self, node):
        if self.is_empty():
            self.queue.append(node)
            return
        for i, other in enumerate(self.queue):
            if other.f >= node.f:
                self.queue.insert(i, node)
                return
        self.queue.append(node)

    def get_node(self, state):
        for node in self.queue:
            if node.state == state:
                return node
        return None

    def pop(self):
        return self.queue.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[0].state

    def is_empty(self):
        return len(self.queue) == 0

    def contains(self, state):
        for node in self.queue:
            if node.state == state:
                return True
        return False

    def get_cost(self, state):
        for node in self.queue:
            if node.state == state:
                return node.g
        return float('inf')


# Grid movement directions: name -> (dx, dy)
DIRECTIONS = {
    'N':  (0,  1),
    'NE': (1,  1),
    'E':  (1,  0),
    'SE': (1, -1),
    'S':  (0, -1),
    'SW': (-1, -1),
    'W':  (-1, 0),
    'NW': (-1, 1),
}

# Fragile cells override the movement cost when entered
FRAGILE_CELLS = {
    (3, 3): 5.0,
    (4, 2): 2.0,
    (3, 4): 3.0,
}

def get_action_cost(next_state, action):
    if next_state in FRAGILE_CELLS:
        return FRAGILE_CELLS[next_state]
    return 1.41 if len(action) == 2 else 1.0


def get_manhattan_distance(pos, goal):
    """|x1-x2| + |y1-y2|"""
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def get_euclidean_distance(pos, goal):
    """sqrt((x1-x2)^2 + (y1-y2)^2)"""
    return math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2)


## You may define more utility functions here


def a_star_search(start_pos, goal_pos, heuristic_type="manhattan", weight=1.0):
    heuristic_fn = get_manhattan_distance if heuristic_type == "manhattan" else get_euclidean_distance

    h0 = heuristic_fn(start_pos, goal_pos)
    start_node = Node(start_pos, parent=None, action=None, g=0.0, h=h0, w=weight)

    frontier = Frontier()
    frontier.push(start_node)
    nodes_generated = 1

    # reached maps each discovered state to the best-known g cost
    reached = ReachedSet()
    reached.add(start_node)

    print(f"=== A* Search ({heuristic_type}) ===")
    print(f"Initial Frontier: [None-->{start_pos}({start_node.g:.2f}, {start_node.f:.2f})]")
    print()

    step = 0
    nodes_expanded = 0

    while not frontier.is_empty():
        node = frontier.pop()

        # Skip stale nodes (a cheaper path to this state was found later)
        if node.g > reached.get_cost(node.state):
            continue

        step += 1
        nodes_expanded += 1

        parent_str = str(node.parent.state) if node.parent else "None"
        print(f"Step {step}")
        print(f"Expanded: {parent_str}-->{node.state}(g={node.g:.2f}, f={node.f:.2f})")

        if node.state == goal_pos:
            path = []
            cur = node
            while cur:
                path.append(cur.state)
                cur = cur.parent
            path.reverse()
            print("\nGoal reached.")
            print(f"Path: {path}")
            print(f"Total estimated cost (f=g+h) = {node.g:.2f}")
            print(f"Nodes expanded = {nodes_expanded}")
            print(f"Nodes generated = {nodes_generated}")
            return path

        for action, (dx, dy) in DIRECTIONS.items():
            nx, ny = node.state[0] + dx, node.state[1] + dy
            if not (1 <= nx <= 5 and 1 <= ny <= 5):
                continue
            next_state = (nx, ny)
            action_cost = get_action_cost(next_state, action)
            new_g = node.g + action_cost
            new_h = heuristic_fn(next_state, goal_pos)

            if not reached.contains(next_state):
                child = Node(next_state, parent=node, action=action, g=new_g, h=new_h, w=weight)
                frontier.push(child)
                reached.add(child)
                nodes_generated += 1
            elif new_g < reached.get_cost(next_state):
                child = Node(next_state, parent=node, action=action, g=new_g, h=new_h, w=weight)
                frontier.push(child)
                reached.update(child)
                nodes_generated += 1

        frontier_str = ", ".join(
            f"{(n.parent.state if n.parent else None)}-->{n.state}({n.g:.2f}, {n.f:.2f})"
            for n in frontier.queue
        )
        print(f"Frontier: [{frontier_str}]")
        print()

    print("No solution found.")
    return None


# Test Case (run twice and compare)
if __name__ == "__main__":
    start = (1, 1)
    goal = (4, 5)

    a_star_search(start, goal, heuristic_type="manhattan", weight=1.0) # modify the weight here for Task 2
    a_star_search(start, goal, heuristic_type="euclidean", weight=1.0) # modify the weight here for Task 2
