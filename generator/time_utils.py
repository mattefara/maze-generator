from .maze import Maze
from .maze_drawer import MazeDrawer, MazeLoader
from . import graph
import time


def elapsed_time(f):
    def compute(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        return (end - start), result
    return compute


@elapsed_time
def generate(size):
    maze = Maze(size)
    maze.generate()
    return maze


@elapsed_time
def load(image_name, colors: tuple):
    wall_color, floor_color, *_ = colors
    return MazeLoader.from_pixels(MazeLoader.to_pixels(image_name), wall_color, floor_color)


@elapsed_time
def draw_maze(maze: Maze, colors=tuple):
    maze_drawer = MazeDrawer(maze, colors)
    maze_drawer.draw()
    return maze_drawer


@elapsed_time
def draw_and_save(image_name: str, maze: Maze, colors=tuple):
    _, maze_drawer = draw_maze(maze, colors)
    maze_drawer.save_as(image_name)
    return maze_drawer


@elapsed_time
def solve_and_save(image_name: str, maze_drawer: MazeDrawer, path_color: tuple = (255, 0, 0)):
    graph = maze_drawer.maze.to_graph()
    path = graph.find_path(maze_drawer.maze.start, maze_drawer.maze.end)
    maze_drawer.draw_path(path, path_color)
    maze_drawer.save_as(image_name)
    return maze_drawer
