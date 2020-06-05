class BestFirstSearch:
	""" Class representing a Best-First search algorithm
	"""

	def __init__(self, maze_graph):
		""" Class constructor

			Args:
				maze_graph: Object representing a maze board in graph format. Check implementation in "Maze.py"
		"""
		self.maze_graph = maze_graph
		self.open = []
		self.closed = []
		