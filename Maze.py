class MazeVertex:
    """ Class used to represent each free-to-walk position in the maze board
    and it's connections as graph vertexes with adjacences list.
    """

    def __init__(self, id, label, adjacence_list=[]):
        """ Class constructor

        Args:
            id (int): The numeric identifier for the vertex
            label (tuple(int, int)): Tuple identifing the vertex position in the maze board indexes (row, column) 
            adjacence_list (list, optional): List of adjacences id's. Defaults to [].
        """
        self.id = id
        self.label = label
        self.adjacence_list = []
        self.h = None # Value used for heuristic informed searches - Best-First Search and A* Search
        self.g = None # Value used for heuristic informed search - A* Search
    
    def add_adjacence(self, neighbour_id):
        """ Method to add the id of a adjacent vertex to this vertex adjacence list

        Args:
            neighbour_id (int): The neighbour vertex id

        Returns:
            Bool: Success of the operation
        """
        if neighbour_id not in self.adjacence_list:
            self.adjacence_list.append(neighbour_id)
            return True
        else:
            print("This adjacence exists already")
            return False

    
    def get_adjacence_list(self):
        """ Returns the adacence list of this vertex

        Returns:
            list[int]: A list with each ajacence vertex id.
        """
        return self.adjacence_list

    def get_id(self):
        """ Returns this vertex id

        Returns:
            int: The vertex id
        """
        return self.id

    def get_label(self):
        """ Returns this vertex label

        Returns:
            tuple(int, int): The vertex label
        """
        return self.label


class MazeGraph:
    """ Class representing the maze as a graph. The class interface is limited to reading methods,
    as all graph information is built from the characters matrix returned from a MazeReader
    "read_from_file" method.
    """
    def __init__(self, maze_as_list_of_lines):
        """ Class constructor

        Args:
            maze_as_list_of_lines (list[list[str]]): A list of lines, each line being a list of strings with lenght 1.
        """
        self.maze_text_info = maze_as_list_of_lines
        self.vertexes_list = []
        self.vertex_id_label_mapping = {} # Helps find a vertex by it's label
        self.root_id = -1 # Vertex id of the maze's starting point
        self.target_id = -1 # Vertex id of the maze's target point
        self.last_added_id = -1 

        self.number_of_rows = len(self.maze_text_info)
        self.number_of_columns = len(self.maze_text_info[0])

        # Ensures the minimal board size
        if (self.number_of_rows < 2) or (self.number_of_columns < 0):
            print("Invalid board dimension. Must be at least 2x2.")
            print("Actual size: {}x{}".format(self.number_of_rows, self.number_of_columns))
            exit(-1)

        self._build_graph_from_text()
    
    def _build_graph_from_text(self):
        """ Private function, automatically called from the constructor. Builds all graph information
            by parsing the string matrix passed to the constructor. At the end of this method execution,
            the properties 'vertexes_list', 'vertex_id_label_mapping', 'root_id' and 'target_id' must be
            properly fullfiled.
        """

        # Parse each board postition type
        for line_index, line_content in zip(range(len(self.maze_text_info)), self.maze_text_info):
            for column_index, column_content in zip(range(len(line_content)), line_content):
                if column_content == '-':
                    continue
                elif column_content == '#':
                    self.root_id = self.last_added_id + 1
                elif column_content == '$':
                    self.target_id = self.last_added_id + 1
                self.last_added_id = self.last_added_id + 1
                self.vertexes_list.append(MazeVertex(self.last_added_id, (line_index, column_index)))
        
        # Create a mapping thus allowing vertexes to be found by label
        self.vertexes_label_to_id_mapping = {vertex.get_label(): vertex.get_id() for vertex in self.vertexes_list}
        
        # Once the vertexes list is done, we can parse the adjacences information
        for vertex in self.vertexes_list:
            (vertex_row, vertex_column) = vertex.get_label()
            adjacences = self._find_vertex_adjacences_from_text(vertex_row, vertex_column)
            for adjacence in adjacences:
                vertex.add_adjacence(adjacence)
        
        # Ensures the board has a starting and ending point
        if (self.root_id == -1):
            print("ERROR: Maze has no starting point.")
            exit(-1)
        if (self.target_id == -1):
            print("ERROR: Maze has no ending point.")
            exit(-1)


    def _find_vertex_adjacences_from_text(self, vertex_row, vertex_column):
        """ Find adjacences information of a vertex using it's board position.

        Args:
            vertex_row (int): Row number the vertex is into.
            vertex_column (int): Column number the vertex is into

        Returns:
            list[int]: List of the adjacences ids.
        """
        found_adjacences = []
        
        if (vertex_row - 1 >= 0):
            if self.maze_text_info[vertex_row - 1][vertex_column] != '-':
               found_adjacences.append(self.vertexes_label_to_id_mapping[(vertex_row - 1, vertex_column)])
        
        if (vertex_column + 1 < self.number_of_columns):
            if self.maze_text_info[vertex_row][vertex_column + 1] != '-':
               found_adjacences.append(self.vertexes_label_to_id_mapping[(vertex_row, vertex_column + 1)])
        
        if (vertex_row + 1 < self.number_of_rows):
            if self.maze_text_info[vertex_row + 1][vertex_column] != '-':
               found_adjacences.append(self.vertexes_label_to_id_mapping[(vertex_row + 1, vertex_column)])

        if (vertex_column - 1 >= 0):
            if self.maze_text_info[vertex_row][vertex_column - 1] != '-':
               found_adjacences.append(self.vertexes_label_to_id_mapping[(vertex_row, vertex_column - 1)])

        return found_adjacences

    def get_vertex_adjacence_by_id(self, vertex_id):
        """ Search the vertex list of adjacences by id

        Args:
            vertex_id (int): The vertex id to search

        Returns:
            list[int]: A list of the adjacences ids
        """
        return self.vertexes_list[vertex_id].get_adjacence_list()

    def get_vertex_adjacence_by_label(self, vertex_label):
        """ Search the vertex list of adjacences by label

        Args:
            vertex_label (int): The vertex label to search

        Returns:
            list[int]: A list of the adjacences ids
        """
        vertex_id = self.vertex_id_label_mapping[vertex_label]
        return self.vertexes_list[vertex_id].get_adjacence_list()



class MazeReader:
    """ A class to read mazes from input files into a format the MazeGraph class can parse.
    """
    def __init__(self):
        pass

    def read_from_file(self, filename):
        """ Given a filename, returns the maze in a representation compatible with MazeGraph class

        Args:
            filename (string): The path to input file

        Returns:
            list[list[string]]: A two dimensional matrix of characters
        """
        try:
            with open(filename) as input_file:
                content = input_file.readlines()
        except Exception as e:
            print("Could not open input file: {}".format(e.args))
            exit(-1)

        maze_board = []
        for line_content in content[1:]:
            line_content = line_content.rstrip('\n')
            maze_line = []
            for block in line_content:
                maze_line.append(block)
            maze_board.append(maze_line)

        return maze_board


if __name__ == "__main__":
    reader = MazeReader()
    maze_as_list_of_lines = reader.read_from_file('./inputs/entrada_1.txt')
    maze_as_graph = MazeGraph(maze_as_list_of_lines)
    
    for vertex in maze_as_graph.vertexes_list:
        print("{}: {}".format(vertex.get_id(), vertex.get_adjacence_list()))