import argparse
import time
import os

from Search import *
from Maze import *

parser = argparse.ArgumentParser(description="Benchmarking e execução de algoritmos de busca em labirintos")
parser.add_argument('--visualize', action='store_true', help="Executa visualização dos algoritmos de busca")
args = parser.parse_args()


inputs_path = 'inputs'
# algs = {"BFS": BreadthFirstSearch, "DFS": DepthFirstSearch, "AS": AStarSearch, "BestFS": BestFirstSearch}
algs = {"BFS": BreadthFirstSearch, "DFS": DepthFirstSearch}

input_file_listage = [os.path.join(inputs_path, name) for name in os.listdir(inputs_path)]

reader = MazeReader()

num_repetitions = 100
time_results = {alg_type: [] for alg_type in algs.keys()}



for alg_type in algs.keys():
    for input_file in input_file_listage:
        maze_as_lines = reader.read_from_file(input_file)
        maze_as_graph = MazeGraph(maze_as_lines)
        searcher = algs[alg_type](maze_as_graph)
        
        init = time.time()
        for i in range(num_repetitions):
            path = searcher.do_search()
        end = time.time()
        avg_time = (end - init) / num_repetitions
        time_results[alg_type].append(avg_time)

print(time_results)
