from search import *
import math
import heapq


class RoutingGraph(Graph):
    
    def __init__(self, map_str):
        self.start_nodes = []
        self.goal_nodes = []
        self.portals = []
        self.block = ['+', '-', 'X', '|']


        map_list = map_str.splitlines()
        self.map_list = [list(i) for i in map_list]

        num_row = len(map_list)
        num_col = len(map_list[0])


        for row in range(num_row):
            for col in range(num_col):
                node = self.map_list[row][col]
##                print(node, type(node))
                
                if node == 'S':
                    self.start_nodes.append((row, col, math.inf))

                elif node == 'G':
                    self.goal_nodes.append((row, col))

                elif node == 'P':
                    self.portals.append((row, col))

                elif node.isdigit():
                    self.start_nodes.append((row, col, int(node)))



    def starting_nodes(self):
        return self.start_nodes



    def is_goal(self, node):
        return (node[0], node[1]) in self.goal_nodes



    def outgoing_arcs(self, node):
        directions = [('N' , -1, 0),
                      ('E' , 0, 1),
                      ('S' , 1, 0),
                      ('W' , 0, -1),]

        arcs = []

        for direction in directions:
            row, col, fuel = node
            
            row += direction[1]
            col += direction[2]

            
            if self.map_list[row][col] not in self.block and fuel > 0:
                head = (row, col, fuel - 1)
                arcs.append(Arc(node, head, direction[0], 5))




        row, col, fuel = node
        if self.map_list[row][col] == 'F' and fuel < 9:
            fuel = 9
            head = (row, col, fuel)
            arcs.append(Arc(node, head, "Fuel up", 15))



        if self.map_list[row][col] == 'P':
            for portal in self.portals:
                
                if (row, col) != portal:
                    row, col = portal
                    head = row, col, fuel
                    arcs.append(Arc(node, head, "Teleport to {}".format(portal), 10))

                
        return arcs



    def estimated_cost_to_goal(self, node):
        path = []

        for row, col in self.goal_nodes:
            path.append((abs(node[0] - row) + abs(node[1] - col)) * 5)
            
        res = min(path)
        return res


class AStarFrontier(Frontier):
    def __init__(self, map_graph):
        self.map_graph = map_graph
        self.container = []
        self.pruning = []
        self.index = 0
        
        heapq.heapify(self.container)



    def add(self, path):
        cost = 0
        for p in path:
            cost += p.cost

        
        arc = path[-1]
##        print(self.map_graph.estimated_cost_to_goal(arc.head))
        
        cost += self.map_graph.estimated_cost_to_goal(arc.head)
        if arc.head not in self.pruning:
            heapq.heappush(self.container, (cost, self.index, path))
            self.index += 1
        

       
    def __iter__(self):
        return self


        
    def __next__(self):
        while len(self.container) > 0:
            res = heapq.heappop(self.container)[2]
            if res[-1].head not in self.pruning:
                self.pruning.append(res[-1].head)
                return res
            
        raise StopIteration


def print_map(map_graph, frontier, solution):
    map_graph = map_graph.map_list

    if solution:
        for path in solution:
            row, col, fuel = path.head
            if map_graph[row][col] == " ":
                map_graph[row][col] = "*"


    for node in frontier.pruning:
        row, col, fuel = node
        if map_graph[row][col] == " ":
            map_graph[row][col] = "."

##    print(map_graph)
    for row in map_graph:
        print("".join(row))












## Testing
map_str = """\
+----------------+
|                |
|                |
|                |
|                |
|                |
|                |
|        S       |
|                |
|                |
|     G          |
|                |
|                |
|                |
+----------------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)




map_str = """\
+----------------+
|                |
|                |
|                |
|                |
|                |
|                |
|        S       |
|                |
|                |
|     G          |
|                |
|                |
|                |
+----------------+
"""


map_graph = RoutingGraph(map_str)
# changing the heuristic so the search behaves like LCFS
map_graph.estimated_cost_to_goal = lambda node: 0

frontier = AStarFrontier(map_graph)

solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)




map_str = """\
+-------------+
| G         G |
|      S      |
| G         G |
+-------------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)




map_str = """\
+-------+
|     XG|
|X XXX  |
|  S    |
+-------+
"""
map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)





map_str = """\
+--+
|GS|
+--+
"""
map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)




map_str = """\
+----+
|    |
| SX |
| X G|
+----+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)



map_str = """\
+---------------+
|    G          |
|XXXXXXXXXXXX   |
|           X   |
|  XXXXXX   X   |
|  X S  X   X   |
|  X        X   |
|  XXXXXXXXXX   |
|               |
+---------------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)




map_str = """\
+---------+
|         |
|    G    |
|         |
+---------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)
##+-----+
##|S    |
##|     |
##|     |
##|XXXXX|
##|     |
##|   G |
##| F   |
##+-----+
##"""    
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)

##map_str = """\
##+---+
##|2 F|
##|XX |
##|X3 |
##|X X|
##|1 X|
##|2  |
##|XX |
##| XF|
##|X  |
##|   |
##|2  |
##|   |
##| G |
##+---+
##"""
##
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)    
##
##print()
##print('Test 10:')
##print()       

##map_str = """\
##+----------------+
##|2              F|
##|XX     G 123    |
##|3XXXXXXXXXXXXXX |
##|  F             |
##|          F     |
##+----------------+
##"""    
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)
##
##print()
##print('Test 11:')
##print()       
##
##map_str = """\
##+-----+
##|S    |
##|     |
##|     |
##|     |
##|     |
##|2  G |
##| F   |
##+-----+
##"""    
##map_graph = RoutingGraph(map_str)
##print(map_graph)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)


##map_str = """\
##+-------+
##|   G   |
##|       |
##|   S   |
##+-------+
##"""
##
##map_graph = RoutingGraph(map_str)
####print(map_graph)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)
##
##
##map_str = """\
##+-------+
##|  GG   |
##|S    G |
##|  S    |
##+-------+
##"""
##
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)
##
##map_str = """\
##+-------+
##|     XG|
##|X XXX  |
##| S     |
##+-------+
##"""
##
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)
##
##
##map_str = """\
##+-------+
##|  F  X |
##|X XXXXG|
##| 3     |
##+-------+
##"""
##
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)
##
##
##map_str = """\
##+--+
##|GS|
##+--+
##"""
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)
##
##
##map_str = """\
##+---+
##|GF2|
##+---+
##"""
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)
##
##
##map_str = """\
##+----+
##| S  |
##| SX |
##|GX G|
##+----+
##"""
##
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)
##
##
##map_str = """\
##+---------+
##|         |
##|    G    |
##|         |
##+---------+
##"""
##
##map_graph = RoutingGraph(map_str)
##frontier = AStarFrontier(map_graph)
##solution = next(generic_search(map_graph, frontier), None)
##print_actions(solution)










##map_str = """\
##+------+
##|S    S|
##|  GXXX|
##|S     |
##+------+
##"""
##
##graph = RoutingGraph(map_str)
##print("Starting nodes:", sorted(graph.starting_nodes()))


##map_str = """\
##+--+
##|GS|
##+--+
##"""
##
##graph = RoutingGraph(map_str)
##
##print("Starting nodes:", sorted(graph.starting_nodes()))
##print("Outgoing arcs (available actions) at the start:")
##for start in graph.starting_nodes():
##    for arc in graph.outgoing_arcs(start):
##        print ("  " + str(arc))
##
##
##
##node = (1,1,1)
##print("\nIs {} goal?".format(node), graph.is_goal(node))
##print("Outgoing arcs (available actions) at {}:".format(node))
##for arc in graph.outgoing_arcs(node):
##    print ("  " + str(arc))


##map_str = """\
##+-------+
##|  9  XG|
##|X XXX P|
##| S  0FG|
##|XX P XX|
##+-------+
##"""
##
##graph = RoutingGraph(map_str)
##
##print("Starting nodes:", sorted(graph.starting_nodes()))
##print("Outgoing arcs (available actions) at starting states:")
##for s in sorted(graph.starting_nodes()):
##    print(s)
##    for arc in graph.outgoing_arcs(s):
##        print ("  " + str(arc))
##
##node = (1,1,5)
##print("\nIs {} goal?".format(node), graph.is_goal(node))
##print("Outgoing arcs (available actions) at {}:".format(node))
##for arc in graph.outgoing_arcs(node):
##    print ("  " + str(arc))
##
##node = (1,7,2)
##print("\nIs {} goal?".format(node), graph.is_goal(node))
##print("Outgoing arcs (available actions) at {}:".format(node))
##for arc in graph.outgoing_arcs(node):
##    print ("  " + str(arc))
##
##node = (3, 7, 0)
##print("\nIs {} goal?".format(node), graph.is_goal(node))
##
##node = (3, 7, math.inf)
##print("\nIs {} goal?".format(node), graph.is_goal(node))
##
##node = (3, 6, 5)
##print("\nIs {} goal?".format(node), graph.is_goal(node))
##print("Outgoing arcs (available actions) at {}:".format(node))
##for arc in graph.outgoing_arcs(node):
##    print ("  " + str(arc))
##
##node = (3, 6, 9)
##print("\nIs {} goal?".format(node), graph.is_goal(node))
##print("Outgoing arcs (available actions) at {}:".format(node))
##for arc in graph.outgoing_arcs(node):
##    print ("  " + str(arc))
##
##node = (2, 7, 4)  # at a location with a portal
##print("\nOutgoing arcs (available actions) at {}:".format(node))
##for arc in graph.outgoing_arcs(node):
##    print ("  " + str(arc))
