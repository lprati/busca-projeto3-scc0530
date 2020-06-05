from Maze import *

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

        first_vertex = maze_graph.vertexes_list[maze_graph.root_id]
        last_vertex = maze_graph.vertexes_list[maze_graph.target_id]

    def do_search(self):
        """ Method that starts a depth-first search over a a graph that represents a maze board game.
            The objective is to find the exit of the maze, given the start position and the exit position.
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
            print("\nFound!")
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

if __name__ == "__main__":
    reader = MazeReader()
    maze_as_list_of_lines = reader.read_from_file('./inputs/entrada_1.txt')
    maze_as_graph = MazeGraph(maze_as_list_of_lines)

    dfs_way = DepthFirstSearch(maze_as_graph)

    dfs_way.print_visited_vertexes()
