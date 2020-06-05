import argparse
import time
import os

from Search import *
from Maze import *

parser = argparse.ArgumentParser(description="Benchmarking e execução de algoritmos de busca em labirintos")
parser.add_argument('--visualize', action='store_true', help="Executa visualização dos algoritmos de busca")
args = parser.parse_args()


inputs_path = 'inputs'
algs = {"BFS": BreadthFirstSearch, "DFS": DepthFirstSearch, "AS": AStarSearch, "BestFS": BestFirstSearch}
# algs = {"BFS": BreadthFirstSearch, "DFS": DepthFirstSearch}

input_file_listage = [os.path.join(inputs_path, name) for name in os.listdir(inputs_path)]

reader = MazeReader()

num_repetitions = 1000
time_results = {alg_type: [] for alg_type in algs.keys()}
maze_results = {alg_type: [] for alg_type in algs.keys()}


for alg_type in algs.keys():
    for input_file in input_file_listage:
        maze_as_lines = reader.read_from_file(input_file)
        maze_as_graph = MazeGraph(maze_as_lines)
        
        init = time.time()
        for i in range(num_repetitions):
            searcher = algs[alg_type](maze_as_graph)
            path = searcher.do_search()
            del searcher
        end = time.time()

        avg_time = (end - init) / num_repetitions
        result_obj = {"dim": (maze_as_graph.number_of_rows, maze_as_graph.number_of_columns), "avg_time": avg_time}
        time_results[alg_type].append(result_obj)

        maze_as_graph.add_solution(path)
        maze_solution_obj = {"dim": (maze_as_graph.number_of_rows, maze_as_graph.number_of_columns), "maze": maze_as_graph}
        maze_results[alg_type].append(maze_solution_obj)

for alg in time_results:
    time_results[alg] = sorted(time_results[alg], key=lambda x : x['avg_time'])
    print(alg)
    for result in time_results[alg]:
        print("{} (per execution, {} repetitions)".format(result, num_repetitions))


if args.visualize:
    for alg in maze_results:
        maze_results[alg] = sorted(maze_results[alg], key=lambda x: x['dim'][1])
        print("VISUALIZING SEARCH FOR {} ALGORITHM".format(alg))
        time.sleep(3)
        for result in maze_results[alg]:
            if result['dim'][0] <= 80 and result['dim'][1] <= 80:
                result['maze'].print_maze()