from cli import start

ONLY_IMAGE = ['images/random_maze_0.png']
RANDOM_GENERATION_15 = ['images/random_maze_1.png', '-g', '15', '15']
RANDOM_GENERATION_DEFAULT = ['images/random_maze_2.png', '-g']
RANDOM_GENERATION_BIG = ['images/random_maze_3.png', '-g', '200', '200']
RANDOM_GENERATION_WITH_PATH = ['images/random_maze_4.png',
                               '-g', '10', '10', '-s', 'images/solved_random_maze_4.png']
RANDOM_GENERATION_SOLVE = ['images/random_maze_5.png', '-g', '10', '10', '-s']

LOAD = ['images/random_maze_0.png', '-l']  # Does nothing
LOAD_SOLVE_WITH_PATH = ['images/random_maze_1.png',
                        '-l', '-s', 'images/result_random_maze_1.png']
LOAD_SOLVE = ['images/random_maze_2.png', '-l', '-s']


samples = [
    ONLY_IMAGE,
    RANDOM_GENERATION_15,
    RANDOM_GENERATION_DEFAULT,
    RANDOM_GENERATION_BIG,
    RANDOM_GENERATION_WITH_PATH,
    RANDOM_GENERATION_SOLVE,
    LOAD,
    LOAD_SOLVE_WITH_PATH,
    LOAD_SOLVE
]

if __name__ == '__main__':
    for sample in samples:
        start(sample)
