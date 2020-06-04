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
    
    def add_adjacence(self, neighbour_id):
        if neighbour_id not in self.adjacence_list:
            self.adjacence_list.append(neighbour_id)
            return True
        else:
            print("This adjacence exists already")
            return False

    def remove_adjacence(self, neighbour_id):
        if neighbour_id in self.adjacence_list:
            self.adjacence_list.remove(neighbour_id)
            return True
        else:
            print("This adjacence does not exist")
            return False
    
    def get_adjacence_list(self):
        return self.adjacence_list

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label


class MazeGraph:
    def __init__(self, maze_as_list_of_lines):

        self.maze_text_info = maze_as_list_of_lines
        self.vertexes_list = []
        self.vertex_mapping_by_id = {}
        self.vertex_id_label_mapping = {}
        self.root_id = 0
        self.target_id = 0
        self.last_added_id = -1

        self.number_of_rows = len(self.maze_text_info)
        self.number_of_columns = len(self.maze_text_info[0])

        if (self.number_of_rows < 2) or (self.number_of_columns < 0):
            print("Invalid board dimension. Must be at least 2x2.")
            print("Actual size: {}x{}".format(self.number_of_rows, self.number_of_columns))
            exit(-1)

        self._build_graph_from_text()
    
    def _build_graph_from_text(self):
        for line_index, line_content in zip(range(len(self.maze_text_info)), self.maze_text_info):
            for column_index, column_content in zip(range(len(line_content)), line_content):
                if column_content == '-':
                    continue
                elif column_content == '#':
                    self.root_id = self.last_added_id + 1
                elif column_content == '$':
                    self.target_id = self.last_added_id + 1
                # Isso roda sempre que o conteudo da coluna nao for '-'
                self.last_added_id = self.last_added_id + 1
                self.vertexes_list.append(MazeVertex(self.last_added_id, (line_index, column_index)))
        
        self.vertexes_label_to_id_mapping = {vertex.get_label(): vertex.get_id() for vertex in self.vertexes_list}
        for vertex in self.vertexes_list:
            (vertex_row, vertex_column) = vertex.get_label()
            adjacences = self._find_vertex_adjacences_from_text(vertex_row, vertex_column)
            for adjacence in adjacences:
                vertex.add_adjacence(adjacence)
            

    def _find_vertex_adjacences_from_text(self, vertex_row, vertex_column):
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
        return self.vertexes_list[vertex_id].get_adjacence_list()

    def get_vertex_adjacence_by_label(self, vertex_label):
        vertex_id = self.vertex_id_label_mapping[vertex_label]
        return self.vertexes_list[vertex_id].get_adjacence_list()



class MazeReader:

    def __init__(self):
        pass

    def read_from_file(self, filename):
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