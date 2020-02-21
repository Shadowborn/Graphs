
# def earliest_ancestor(ancestors, starting_node):
#     pass

# gonna want to have the Graph  and Queue class in here
# copied from graph project :)


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        """
        if vertex not in self.vertices:
            self.vertices[vertex] = set()
            # TODO

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Cannot create edge based upon current vertices")


def earliest_ancestor(ancestors, starting_node):
    # ancestors getting passed in as pairs of vertices
    # parent->child
    # let's create a graph that connects all of the people together
    family = Graph()
    # original data is parent->child pairs
    for parentChild in ancestors:
        family.add_vertex(parentChild[0])
        family.add_vertex(parentChild[1])
        # we need to add an edge here - but if we are going to be swimming upstream, we should link them backwards
        family.add_edge(parentChild[1], parentChild[0])

    # let's create a list of paths(lists) that trace upstream to the parents
    paths = Queue()
    paths.enqueue([starting_node])
    # we should do a BFS from starting node to the last node available -- this should be compared
    # to other paths we find
    # default situation is that there's no ancestor
    ancestor = -1
    # default distance to ancestor is one (cause default there is no ancestor but the distance is still one to get to -1)
    longestPath = 1
    # THE FUN PART...

    # as long as we've still got paths to check out...
    while paths.size() > 0:
        # look at first path in line
        path = paths.dequeue()
        # the ancestor we are looking at is the one at the end of the path (farthest upstream). If this is the first time going through this process, the child is the "parent"
        parent = path[-1]
        # if our path is longer than what we had before, we've got an older ancestor and update the longest path
        # also we need to check if we have a split-parenting thing going on where the length is the same, and make the lowest number the ancestor
        if ((len(path) >= longestPath) and (parent < ancestor)) or (len(path) > longestPath):
            longestPath = len(path)
            ancestor = parent

            # get the next parent(s) upstream (if any) and add them to new copy(ies) of the path list
        for adult in family.vertices[parent]:
            newPath = list(path)
            newPath.append(adult)
            paths.enqueue(newPath)

    return ancestor


'''
       10
     /
    1   2   4  11
     \ /   / \ /
      3   5   8
       \ / \   \
        6   7   9
'''
test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
                  (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

print("ancestor of 1 (should be 10): ", earliest_ancestor(test_ancestors, 1))
print("ancestor of 2 (should be -1): ", earliest_ancestor(test_ancestors, 2))
print("ancestor of 3 (should be 10): ", earliest_ancestor(test_ancestors, 3))
print("ancestor of 4 (should be -1): ", earliest_ancestor(test_ancestors, 4))
print("ancestor of 5 (should be 4): ", earliest_ancestor(test_ancestors, 5))
print("ancestor of 6 (should be 10): ", earliest_ancestor(test_ancestors, 6))
print("ancestor of 7 (should be 4): ", earliest_ancestor(test_ancestors, 7))
print("ancestor of 8 (should be 4): ", earliest_ancestor(test_ancestors, 8))
print("ancestor of 9 (should be 4): ", earliest_ancestor(test_ancestors, 9))
print("ancestor of 10 (should be -1): ", earliest_ancestor(test_ancestors, 10))
print("ancestor of 11 (should be -1): ", earliest_ancestor(test_ancestors, 11))