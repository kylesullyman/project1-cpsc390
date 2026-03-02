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
    # 0th index as head of queue
    def __init__(self):
        self.queue = []

    def push(self, node):
        for otherNode in self.queue:
            if otherNode.evalCost >= node.evalCost:
                continue
            else:
                indexToAppend = self.queue.index(otherNode)
                self.queue.insert(indexToAppend, node)
                break

    def pop(self):
        return self.queue.pop(0)

    def peek(self):
        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    

#TODO: Compete this
def get_manhattan_distance(pos, goal):
    """|x1-x2| + |y1-y2|"""

    pass

#TODO: Complete this
def get_euclidean_distance(pos, goal):
    """sqrt((x1-x2)^2 + (y1-y2)^2)"""

    pass

## You may define more utility functions here




#TODO: Complete this
def a_star_search(start_pos, goal_pos, heuristic_type="manhattan", weight = 1.0):

    pass


# Test Case (run twice and compare)
if __name__ == "__main__":
    start = (1, 1)
    goal = (4, 5)

    a_star_search(start, goal, heuristic_type="manhattan", weight=1.0) # modify the weight here for Task 2
    a_star_search(start, goal, heuristic_type="euclidean", weight=1.0) # modify the weight here for Task 2