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

        # Get an heuristic value for each vertex.
        # Current heuristic is the euclidian distance between vertex and target vertex
        (target_vertex_row, target_vertex_column) = self.maze_graph.vertexes_list[self.maze_graph.target_id].get_label()
        for current_vertex in self.maze_graph.vertexes_list:
            (vertex_row, vertex_column) = current_vertex.get_label()
            diff_x = (target_vertex_row - vertex_row) ** 2
            diff_y = (target_vertex_column - vertex_column) ** 2
            current_vertex.h = math.ceil(math.sqrt(diff_x + diff_y))

    def do_search(self):
        first_vertex = self.maze_graph.vertexes_list[self.maze_graph.root_id]
        self.open.put((first_vertex.h, first_vertex.id, first_vertex))

        # Step 1: 
        while self.open.empty() == False:
            current_vertex = self.open.get()[2]
            # Step 2: Add current vertex to closed vertexes list 
            self.closed.append(current_vertex.get_label())

            # Step 2: Found way out
            if current_vertex.h == 0:
                print("\nFound!")
                return self.closed

            # Step 3: Didn't find way out. Looks in adjacences
            for neighbor_id in current_vertex.get_adjacence_list():
                neighbor_vertex = self.maze_graph.vertexes_list[neighbor_id]

                # Step 3.1: Add neighbor vertex in open vertexes queue
                if neighbor_vertex.get_label() not in self.closed:
                    self.open.put((neighbor_vertex.h, neighbor_vertex.id, neighbor_vertex))

        # Step 4: If target vertex was not found, the search was a failure
        return None

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
