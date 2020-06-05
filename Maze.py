import curses
import time

class MazeVertex:
    """ Class used to represent each free-to-walk position in the maze board
    and it's connections as graph vertexes with adjacences list.
    """

    def __init__(self, id, label, adjacence_list=[], parent=None):
        """ Class constructor

        Args:
            id (int): The numeric identifier for the vertex
            label (tuple(int, int)): Tuple identifing the vertex position in the maze board indexes (row, column) 
            adjacence_list (list, optional): List of adjacences id's. Defaults to [].
        """
        self.id = id
        self.label = label
        self.adjacence_list = []
        self.parent = parent # Parent of a given path - used in Best-First Search and A* Search
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

    def add_solution(self, list_of_positions):
        self.solution_path = list_of_positions

    def print_maze(self):
        curses.wrapper(self._wraped_print_maze)

    def _wraped_print_maze(self, stdscr):
    
        start_pos = self.vertexes_list[self.root_id].get_label()
        end_pos = self.vertexes_list[self.target_id].get_label()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)     # Walls
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)     # Paths
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)      # Start
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)       # End
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_YELLOW)    # Visited
        
        stdscr.clear()
        stdscr.nodelay(1)

        for line_index, line in zip(range(len(self.maze_text_info)),self.maze_text_info):
            for column_index, column in zip(range(len(line)),line):
                if column == '-':
                    color = curses.color_pair(1)
                elif column == '*':
                    color = curses.color_pair(2)
                elif column == '#':
                    color = curses.color_pair(3)
                elif column == '$':
                    color = curses.color_pair(4) 
                stdscr.addstr(line_index, column_index, ' ', color)
        stdscr.refresh()
        time.sleep(0.5)

        for walked in self.solution_path:
            stdscr.addstr(walked[0], walked[1], ' ', curses.color_pair(5))
            stdscr.addstr(start_pos[0], start_pos[1], ' ', curses.color_pair(3))
            stdscr.addstr(end_pos[0], end_pos[1], ' ', curses.color_pair(4))
            stdscr.refresh()
            time.sleep(0.01)
        stdscr.nodelay(0)
        stdscr.getch()

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
