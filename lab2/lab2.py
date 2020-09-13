# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    agenda = [ [start] ]

    while len(agenda) > 0:
        path = agenda.pop(0)
        
        parent = path[len(path) - 1]

        if parent == goal and graph.is_valid_path(path):
            return path

        childs = graph.get_connected_nodes(parent)

        for node in childs:
            if node in path:
                continue

            new_path = list(path)
            new_path.append(node)

            # algorithms differ here
            agenda.append(new_path)

    return []
        

       

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    agenda = [ [start] ]

    while len(agenda) > 0:
        path = agenda.pop(0)
        
        parent = path[len(path) - 1]

        if parent == goal and graph.is_valid_path(path):
            return path

        childs = graph.get_connected_nodes(parent)

        for node in childs:
            if node in path:
                continue

            new_path = list(path)
            new_path.append(node)

            # algorithms differ here
            agenda.insert(0, new_path)

    return []


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    agenda = [ [start] ]

    while len(agenda) > 0:
        path = agenda.pop(0)
        
        parent = path[len(path) - 1]

        if parent == goal and graph.is_valid_path(path):
            return path

        childs = graph.get_connected_nodes(parent)
        childs.sort(key=lambda c: graph.get_heuristic(c, goal), reverse=True)

        for node in childs:
            if node in path:
                continue

            new_path = list(path)
            new_path.append(node)

            # algorithms differ here
            agenda.insert(0, new_path)

    return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    agenda = [ [start] ]
    agenda_len = 1

    while len(agenda) > 0:
        path = agenda.pop(0)
        
        parent = path[len(path) - 1]

        if parent == goal and graph.is_valid_path(path):
            return path

        childs = graph.get_connected_nodes(parent)

        for node in childs:
            if node in path:
                continue

            new_path = list(path)
            new_path.append(node)

            # algorithms differ here
            agenda.append(new_path)
        
        if len(agenda) > 0 and len(agenda[0]) > agenda_len:
            agenda.sort(key=lambda path: graph.get_heuristic(path[len(path)-1], goal))
            agenda = agenda[:beam_width]
            agenda_len += 1

    return []

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    res = 0

    if len(node_names) < 2:
        return res

    for i in range(1, len(node_names)):
        prev = node_names[i - 1]
        curr = node_names[i]
        edge = graph.get_edge(prev, curr)
        res += edge.length
    return res


def branch_and_bound(graph, start, goal):
    agenda = [ [start] ]

    while len(agenda) > 0:
        path = agenda.pop(0)
        
        parent = path[len(path) - 1]

        if parent == goal and graph.is_valid_path(path):
            return path

        childs = graph.get_connected_nodes(parent)

        for node in childs:
            if node in path:
                continue

            new_path = list(path)
            new_path.append(node)

            # algorithms differ here
            agenda.append(new_path)

        agenda.sort(key=lambda p: path_length(graph, p))

    return []

def a_star(graph, start, goal):
    agenda = [ [start] ]
    extended_set = []
    while len(agenda) > 0:
        path = agenda.pop(0)
        
        parent = path[len(path) - 1]

        if parent == goal and graph.is_valid_path(path):
            return path

        childs = graph.get_connected_nodes(parent)

        for node in childs:
            if node in path:
                continue

            if node in extended_set:
                continue

            new_path = list(path)
            new_path.append(node)

            # algorithms differ here
            agenda.append(new_path)
            extended_set.append(node)
            
        agenda.sort(key=lambda p: path_length(graph, p) + graph.get_heuristic(p[len(p)-1], goal))

    return []



## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    agenda = [ [goal] ]
    extended_set = []

    while len(agenda) > 0:
        path = agenda.pop(0)

        parent = path[len(path) - 1]

        if (path_length(graph, path) < graph.get_heuristic(parent, goal)):
            return False

        if parent in extended_set:
            continue

        extended_set.append(parent)

        childs = graph.get_connected_nodes(parent)

        for node in childs:
            if node in path:
                continue

            new_path = list(path)
            new_path.append(node)

            # algorithms differ here
            agenda.append(new_path)

    return True

def is_consistent(graph, goal):
    agenda = [ goal ]
    extended_set = []

    while len(agenda) > 0:
        parent = agenda.pop(0)

        if parent in extended_set:
            continue

        extended_set.append(parent)
        
        childs = graph.get_connected_nodes(parent)

        for child in childs:
            edge = graph.get_edge(parent, child)
            h_parent = graph.get_heuristic(parent, goal)
            h_child = graph.get_heuristic(child, goal)

            if edge.length < abs(h_child - h_parent):
                return False

            agenda.append(child)

    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '4'
WHAT_I_FOUND_INTERESTING = 'Everything'
WHAT_I_FOUND_BORING = 'Nothing'
