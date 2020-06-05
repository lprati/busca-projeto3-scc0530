from Maze import *
import math
from queue import PriorityQueue

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

            # We have a g variable in A* algorithm, that helps us calculate the best choice
            # between neighbors of a given vertex
            current_vertex.g = 0

    def do_search(self):
        """ Runs A* Search.

            Returns:
                list[tuple(int, int)]: list of traversed vertex labels
        """

        first_vertex = self.maze_graph.vertexes_list[self.maze_graph.root_id]
        self.open.put((self._calculate_f(first_vertex), first_vertex.id, first_vertex))

        # Step 1: 
        while self.open.empty() == False:
            current_vertex = self.open.get()[2]
            # Step 2: Add current vertex to closed vertexes list 
            self.closed.append(current_vertex.get_label())

            # Step 2: Found way out
            if current_vertex.id == self.maze_graph.target_id:
                print("\nFound!")
                return self.closed

            # Step 4: Didn't find way out. Looks in adjacences
            for neighbor_id in current_vertex.get_adjacence_list():
                neighbor_vertex = self.maze_graph.vertexes_list[neighbor_id]

                # Step 4.1: New g for neighbor vertex
                neighbor_vertex.g = current_vertex.g + 1

                # Step 4.2: Add neighbor vertex in open vertexes queue
                if neighbor_vertex.get_label() not in self.closed:
                    self.open.put((self._calculate_f(neighbor_vertex), neighbor_vertex.id, neighbor_vertex))

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


if __name__ == "__main__":
    reader = MazeReader()
    maze_as_list_of_lines = reader.read_from_file('./inputs/entrada_1.txt')
    maze_as_graph = MazeGraph(maze_as_list_of_lines)

    best_first_way = BestFirstSearch(maze_as_graph)
    best_first_way.print_visited_vertexes()
