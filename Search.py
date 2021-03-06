import math
from queue import PriorityQueue

from Maze import *

class AStarSearch:
    """ Class representing a Best-First search algorithm
    """

    def __init__(self, maze_graph):
        """ Class constructor

            Args:
                maze_graph: Object representing a maze board in graph format. Check implementation in "Maze.py"
        """
        self.maze_graph = maze_graph
        self.open = PriorityQueue()
        self.closed = []
        self.path = []

        # Get an heuristic value for each vertex.
        # Current heuristic is the euclidian distance between vertex and target vertex
        (target_vertex_row, target_vertex_column) = self.maze_graph.vertexes_list[self.maze_graph.target_id].get_label()
        for current_vertex in self.maze_graph.vertexes_list:
            (vertex_row, vertex_column) = current_vertex.get_label()
            diff_x = (target_vertex_row - vertex_row) ** 2
            diff_y = (target_vertex_column - vertex_column) ** 2
            current_vertex.h = math.ceil(math.sqrt(diff_x + diff_y))

            # We have a g variable in A* algorithm, that helps us calculate the best choice
            # between neighbors of a given vertex
            current_vertex.g = 0

    def do_search(self):
        """ Runs Best-First Search

            Returns:
                list[tuple(int, int)]: list of traversed vertex labels
        """

        first = self.maze_graph.vertexes_list[self.maze_graph.root_id]
        first_vertex = MazeVertex(first.id, first.label, None, None)
        first_vertex.adjacence_list = first.get_adjacence_list()
        first_vertex.h = first.h
        first_vertex.g = first.g
        self.open.put((self._calculate_f(first_vertex), first_vertex.id, first_vertex))

        # Step 1: 
        while self.open.empty() == False:
            current_vertex = self.open.get()[2]
            # Step 2: Add current vertex to closed vertexes list 
            self.closed.append(current_vertex.get_label())

            # Step 3: Found way out
            if current_vertex.id == self.maze_graph.target_id:

                #Step 3.1: Traverse path
                current_path = current_vertex
                while current_path != None:
                    self.path.append(current_path.get_label())
                    current_path = current_path.parent

                self.path.reverse()                    
                return self.path

            # Step 4: Didn't find way out. Looks in adjacences
            for neighbor_id in current_vertex.get_adjacence_list():
                neighbor = self.maze_graph.vertexes_list[neighbor_id]
                path_vertex = MazeVertex(neighbor.id, neighbor.label, None, current_vertex)
                path_vertex.adjacence_list = neighbor.get_adjacence_list()
                path_vertex.parent = current_vertex
                path_vertex.h = neighbor.h
                path_vertex.g = current_vertex.g + 1

                # Step 4.1: Add neighbor vertex in open vertexes queue
                if path_vertex.get_label() not in self.closed:
                    # Check if it is in open queue
                    q = self.open.queue
                    to_insert = (self._calculate_f(path_vertex), path_vertex.id, path_vertex)
                    already_in_open = False

                    for item in q:
                        (f, vertex_id, parent) = item
                        if f == to_insert[0] and vertex_id == to_insert[1]:
                            already_in_open = True
                            break
                    if already_in_open == False:
                        self.open.put(to_insert)

        # Step 5: If target vertex was not found, the search was a failure
        return None

    def _calculate_f(self, vertex):
        """ Private method that calculates F

            returns:
                F: h + g
        """
        return vertex.h + vertex.g


    def print_visited_vertexes(self):
        """ Prints all id's of the vertexes representing the way out of the maze 
        """

        way_out = "Way out of maze: "
        for visited_vertex in self.do_search():
            way_out = way_out + "{} -> ".format(visited_vertex)
        way_out = way_out + "end!"
        print(way_out)


class BestFirstSearch:
    """ Class representing a Best-First search algorithm
	"""

    def __init__(self, maze_graph):
        """ Class constructor
            Args:
                maze_graph: Object representing a maze board in graph format. Check implementation in "Maze.py"
        """
        self.maze_graph = maze_graph
        self.open = PriorityQueue()
        self.closed = []
        self.path = []

        # Get an heuristic value for each vertex.
        # Current heuristic is the euclidian distance between vertex and target vertex
        (target_vertex_row, target_vertex_column) = self.maze_graph.vertexes_list[self.maze_graph.target_id].get_label()
        for current_vertex in self.maze_graph.vertexes_list:
            (vertex_row, vertex_column) = current_vertex.get_label()
            diff_x = (target_vertex_row - vertex_row) ** 2
            diff_y = (target_vertex_column - vertex_column) ** 2
            current_vertex.h = math.ceil(math.sqrt(diff_x + diff_y))

    def do_search(self):
        """ Runs Best-First Search
            Returns:
                list[tuple(int, int)]: list of traversed vertex labels
        """

        first = self.maze_graph.vertexes_list[self.maze_graph.root_id]
        first_vertex = MazeVertex(first.id, first.label, None, None)
        first_vertex.adjacence_list = first.get_adjacence_list()
        first_vertex.h = first.h
        self.open.put((self._calculate_f(first_vertex), first_vertex.id, first_vertex))

        # Step 1: 
        while self.open.empty() == False:
            current_vertex = self.open.get()[2]
            # Step 2: Add current vertex to closed vertexes list 
            self.closed.append(current_vertex.get_label())

            # Step 3: Found way out
            if current_vertex.id == self.maze_graph.target_id:

                #Step 3.1: Traverse path
                current_path = current_vertex
                while current_path != None:
                    self.path.append(current_path.get_label())
                    current_path = current_path.parent

                self.path.reverse()                    
                return self.path

            # Step 4: Didn't find way out. Looks in adjacences
            for neighbor_id in current_vertex.get_adjacence_list():
                neighbor = self.maze_graph.vertexes_list[neighbor_id]
                path_vertex = MazeVertex(neighbor.id, neighbor.label, None, current_vertex)
                path_vertex.adjacence_list = neighbor.get_adjacence_list()
                path_vertex.parent = current_vertex
                path_vertex.h = neighbor.h

                # Step 4.1: Add neighbor vertex in open vertexes queue
                if path_vertex.get_label() not in self.closed:
                    # Check if it is in open queue
                    q = self.open.queue
                    to_insert = (self._calculate_f(path_vertex), path_vertex.id, path_vertex)
                    already_in_open = False

                    for item in q:
                        (f, vertex_id, parent) = item
                        if f == to_insert[0] and vertex_id == to_insert[1]:
                            already_in_open = True
                            break
                    if already_in_open == False:
                        self.open.put(to_insert)

        # Step 5: If target vertex was not found, the search was a failure
        return None

    def _calculate_f(self, vertex):
        """ Private method that calculates F
            returns:
                F: h 
        """
        return vertex.h


    def print_visited_vertexes(self):
        """ Prints all id's of the vertexes representing the way out of the maze 
        """

        way_out = "Way out of maze: "
        for visited_vertex in self.do_search():
            way_out = way_out + "{} -> ".format(visited_vertex)
        way_out = way_out + "end!"
        print(way_out)


class BreadthFirstSearch:
    def __init__(self, maze_graph):
        """ Class to run BFS over a given MazeGraph object

        Args:
            maze_graph (object MazeGraph): Maze to solve
        """

        self.maze_graph = maze_graph
        self.visited = [False for vertex in maze_graph.vertexes_list]
        self.queue = []
        self.found = False

    def do_search(self):
        """ Runs BFS search

        Returns:
            list[tuple(int, int)]: List of the traversed vertexes labels
        """
        self.queue.append(self.maze_graph.root_id)
        self.visited[self.maze_graph.root_id] = True
        path = []

        while len(self.queue) > 0 and self.found == False:
            v = self.queue.pop(0)
            path.append(self.maze_graph.vertexes_list[v].get_label())

            for index in self.maze_graph.get_vertex_adjacence_by_id(v):
                if index == self.maze_graph.target_id:
                    self.found=True
                if self.visited[index] == False:
                    self.queue.append(index)
                    self.visited[index] = True
        
        return path


class DepthFirstSearch:
    """ Class representing a depth first search in a given graph.
    """

    def __init__(self, maze_graph):
        """ Class constructor
                        
            Args:
                maze_graph: Object representing a maze board in graph format. Check implementation in "Maze.py"
        """
        self.maze_graph = maze_graph
        self.visited = []
        self.has_found = False

    def do_search(self):
        """ Method that starts a depth-first search over a a graph that represents a maze board game.
            The objective is to find the exit of the maze, given the start position and the exit position.

            Returns:
                list[tuple(int, int)]: List of traversed vertexes labels
        """
        first_vertex = self.maze_graph.vertexes_list[self.maze_graph.root_id]

        self._depth_first_search(first_vertex)
        return self.visited

    def _depth_first_search(self, maze_vertex):
        """ Private method that makes a recursion of a depth-first search over a graph that represents
            a maze board game.  
        
            Args:
                maze_graph: maze board represented by a graph structure
                maze_vertex: current visited position in maze, represented by a graph vertex
        """
        # Trivial case 1: has found in another branch
        if (self.has_found == True):
            return

        # Saves visited vertex in set (for better search performance)
        # and 
        self.visited.append(maze_vertex.get_label())

        # Trivial case 2: found exit
        if (maze_vertex.id == self.maze_graph.target_id):
            self.has_found = True
            return

        for next_tile_id in maze_vertex.get_adjacence_list():
            next_tile_as_vertex = self.maze_graph.vertexes_list[next_tile_id]

            # If the tile was not visited yet, do another recursion to the next tile
            if not next_tile_as_vertex.get_label() in self.visited:
              self._depth_first_search(next_tile_as_vertex)

    def print_visited_vertexes(self):
        """ Prints all id's of the vertexes representing the way out of the maze 
        """

        way_out = "Way out of maze: "
        for visited_vertex in self.do_search():
            way_out = way_out + "{} -> ".format(visited_vertex)
        way_out = way_out + "end!"
        print(way_out)