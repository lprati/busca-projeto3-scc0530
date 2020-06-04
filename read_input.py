class MazeVertex:
    """ Class used to represent each free-to-walk position in the maze board
    and it's connections as graph vertexes with adjacences list.
    """

    def init(self, id, label, adjacence_list=[]):
        """ Class constructor

        Args:
            id (int): The numeric identifier for the vertex
            label ([type]): [description]
            adjacence_list (list, optional): [description]. Defaults to [].
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
    
    def return_adjacence(self):
        return self.adjacence_list


class MazeGraph:
    def init(self, maze_as_list_of_lines):

        self.maze_text_info = maze_as_list_of_lines
        self.vertixes_list = []
        self.root_id = 0
        self.target_id = 0
        self.last_added_id = -1

        self._build_graph_from_text()
    
    def _build_graph_from_text(self):
        pass
    
    def get_vertex_adjacence(self, vertex_id):
        pass

    def set_vertex_adjacence(self, vertex_id, list_of_adjacences):
        pass



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
    print(maze_as_list_of_lines)