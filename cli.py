import argparse
import types
from random import randint
from generator.time_utils import draw_and_save, generate, load, solve_and_save, draw_maze
import maze_config as cfg

parser = argparse.ArgumentParser()


def generate_solved_name(image_path: str) -> str:
    parts = image_path.split('/')
    prefix = 'solved'
    if len(parts) == 1:
        parts = image_path.split('\\')
    parts[len(parts) - 1] = f'{prefix}_{parts[len(parts) - 1]}'
    return '/'.join(parts)


def start(options: list = None):
    if options is not None:
        args = parser.parse_args(options)
    else:
        args = parser.parse_args()

    maze = None

    initializing_maze_time = 0
    action = 'generate'
    colors = (cfg.WALL_COLOR, cfg.FLOOR_COLOR, cfg.END_POINT_COLOR)
    if args.generate is not None and len(args.generate) not in (0, 2):
        parser.error(
            f'Either give no values for generate, or two, not {len(args.generate)}.')

    if args.generate is not None:
        maze_size = args.generate
        if len(args.generate) == 0:
            maze_size = [10, 10]
        image_path_source = args.image_path
        print(f'Generating flag enabled... Generating a {maze_size} maze')
        initializing_maze_time, maze = generate(maze_size)
    elif args.load:
        image_path_source = args.image_path
        initializing_maze_time, maze = load(image_path_source, colors)
        action = 'load'
        print('Load flag enabled... Loading from')
    else:
        maze_size = [10, 10]
        print(
            f'Neither load or generate flags specified... Generating a {maze_size} maze...')
        initializing_maze_time, maze = generate(maze_size)
        image_path_source = args.image_path

    print(f'Done initializing the maze in {initializing_maze_time}')

    maze_draw_time = .0
    if action == 'generate':
        maze_draw_time, maze_drawer = draw_and_save(
            image_path_source, maze, colors)
    elif action == 'load':
        maze_draw_time, maze_drawer = draw_maze(maze, colors)
    else:
        print('Action not supported')

    print(f'Maze drawn in {maze_draw_time} ')

    if args.solution_path:
        solve_result_image = None
        if isinstance(args.solution_path, str):
            solve_result_image = args.solution_path
            print('Argument -s IMAGE_PATH specified')
        elif isinstance(args.solution_path, types.FunctionType):
            print('Argument -s without IMAGE_PATH specified, generating a new one')
            solve_result_image = args.solution_path(args.image_path)

        print(f'Solve path: {solve_result_image}')

        solving_time, maze_drawer = solve_and_save(
            solve_result_image, maze_drawer)
        print(f'Solved and saved in {solving_time}')

    else:
        print('No solution image found')


parser.add_argument('image_path', help='The source of the image')

group = parser.add_mutually_exclusive_group()

group.add_argument(
    '-l', '--load', help='Load maze from image', action='store_true')
group.add_argument('-g', '--generate', metavar='N', action='store',
                   help='Generate a new maze', nargs='*', type=int)
parser.add_argument('-s', '--solve', dest='solution_path', const=generate_solved_name,
                    default=None, nargs='?', help='Solve from image or from generate maze')


if __name__ == '__main__':
    start()
