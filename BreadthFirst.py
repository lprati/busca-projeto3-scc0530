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

    def run_search(self):
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
                    print("\nFound!")
                    self.found=True
                if self.visited[index] == False:
                    self.queue.append(index)
                    self.visited[index] = True
        
        return path

