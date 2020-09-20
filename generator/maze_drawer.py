import numpy as np
from PIL import Image, ImageDraw
from .maze import Maze


class MazeLoader:

    @staticmethod
    def from_pixels(pixels: list, wall_color: tuple, floor_color: tuple) -> Maze:
        maze_start_y, maze_start_x, * \
            _ = np.unravel_index(np.argmax(pixels == list(
                wall_color), axis=None), pixels.shape)

        print(f'Start position at: {(maze_start_x, maze_start_y)}')
        entrance_indexes = np.unique(
            np.where(pixels[maze_start_y] == floor_color)[0])

        cell_size = len(entrance_indexes) + 2
        print(f'Cell size {cell_size}')

        maze_size = pixels.shape[1] - \
            (np.argmax(pixels[maze_start_y][:-1] == list(wall_color)))
        print(f'Maze size: {maze_size}')

        middle = cell_size // 2

        size = (maze_size // cell_size, maze_size // cell_size)

        maze = Maze(size)

        sides = {}
        for room in maze:
            y, x = room.get_position()

            sides[Maze.Room.Side.TOP] = (
                maze_start_x + cell_size * x + middle, maze_start_y + cell_size * y)
            sides[Maze.Room.Side.RIGHT] = (
                maze_start_x + cell_size * x + cell_size, maze_start_y + cell_size * y + middle)
            sides[Maze.Room.Side.BOTTOM] = (
                maze_start_x + cell_size * x + middle, maze_start_y + cell_size * y + cell_size)
            sides[Maze.Room.Side.LEFT] = (
                maze_start_x + cell_size * x, maze_start_y + cell_size * y + middle)

            current_room_type = Maze.Room.Type.VISITED

            for side, _ in room:
                _x, _y = sides[side]
                if tuple(pixels[_y][_x]) == floor_color:
                    room.set_side(side, False)

            if y == 0 and room.get_side(Maze.Room.Side.TOP) == False:
                maze.start = (y, x)
                current_room_type = Maze.Room.Type.END_POINT
                print(f' ----- Start at: {x,y}')

            if y == maze.rows-1 and room.get_side(Maze.Room.Side.BOTTOM) == False:
                maze.end = (y, x)
                current_room_type = Maze.Room.Type.END_POINT
                print(f' ----- Start end: {x,y}')

            maze.set_room_type(room, current_room_type)

        return maze

    @staticmethod
    def load(image_name: str) -> Image:
        return Image.open(image_name)

    @staticmethod
    def to_pixels(image_name: str) -> list:
        image = MazeLoader.load(image_name)
        pixels = np.asarray(image, dtype=tuple)
        return pixels


class MazeDrawer:

    def __init__(self, maze: Maze, colors: tuple = (), cell_size=20, linewidth=2, offset=(0, 0)):
        self.maze = maze
        wall_color, floor_color, end_point_color, *_ = colors
        self.colors = {
            Maze.Room.Type.WALL: wall_color,
            Maze.Room.Type.VISITED: floor_color,
            Maze.Room.Type.END_POINT: end_point_color,
        }
        self.line_width = max(1, linewidth)
        self.offset = offset
        self.cell_size = max(5, cell_size)
        self.drawing_surface = Image.new('RGB', (maze.cols * cell_size + linewidth,
                                                 maze.rows * cell_size + linewidth), self.colors[Maze.Room.Type.VISITED])

    def draw(self) -> None:
        draw = ImageDraw.Draw(self.drawing_surface)
        for room in self.maze:
            y, x = self.offset[1] + self.cell_size * room.get_position(
            )[0], self.offset[0] + self.cell_size * room.get_position()[1]
            for side, value in room:
                color = self.colors[Maze.Room.Type.WALL]
                if side == Maze.Room.Side.TOP and value == True:
                    draw.line((x, y) + (x + self.cell_size +
                                        self.line_width // 2, y), color, self.line_width)
                elif side == Maze.Room.Side.RIGHT and value == True:
                    draw.line((x + self.cell_size + self.line_width // 2, y + self.cell_size + self.line_width //
                               2) + (x + self.cell_size + self.line_width // 2, y), color, self.line_width)
                elif side == Maze.Room.Side.LEFT and value == True:
                    draw.line((x, y) + (x, y + self.cell_size +
                                        self.line_width // 2), color, self.line_width)
                elif side == Maze.Room.Side.BOTTOM and value == True:
                    draw.line((x + self.cell_size + self.line_width // 2, y + self.cell_size + self.line_width // 2) + (
                        x + self.line_width // 2, y + self.cell_size + self.line_width // 2), color, self.line_width)

    def draw_path(self, path: list, path_color: tuple):
        draw = ImageDraw.Draw(self.drawing_surface)

        def draw_line(position, direction) -> tuple:
            y, x = position
            if direction == Maze.Room.Side.TOP:
                return (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), (x * self.cell_size + self.cell_size // 2, y * self.cell_size)
            elif direction == Maze.Room.Side.RIGHT:
                return (x * self.cell_size + self.cell_size // 2 - self.line_width // 2, y * self.cell_size + self.cell_size // 2), (x * self.cell_size + self.cell_size + self.line_width // 2, y * self.cell_size + self.cell_size // 2)
            elif direction == Maze.Room.Side.LEFT:
                return (x * self.cell_size + self.cell_size // 2,  y * self.cell_size + self.cell_size // 2 + self.line_width // 2), (x * self.cell_size, y * self.cell_size + self.cell_size // 2 + self.line_width // 2)
            elif direction == Maze.Room.Side.BOTTOM:
                return (x * self.cell_size + self.cell_size // 2 - self.line_width // 2, y * self.cell_size + self.cell_size // 2), (x * self.cell_size + self.cell_size // 2 - self.line_width // 2, y * self.cell_size + self.cell_size)

        def determine_direction(p1, p2):
            p1_y, p1_x = p1
            p2_y, p2_x = p2
            if p1_x == p2_x:
                if p1_y < p2_y:
                    return Maze.Room.Side.BOTTOM
                else:
                    return Maze.Room.Side.TOP
            elif p1_y == p2_y:
                if p1_x < p2_x:
                    return Maze.Room.Side.RIGHT
                else:
                    return Maze.Room.Side.LEFT
            return None

        start_x, end_x = draw_line(self.maze.start, Maze.Room.Side.TOP)
        draw.line(start_x + end_x, path_color, self.line_width)
        start_x, end_x = draw_line(self.maze.end, Maze.Room.Side.BOTTOM)
        draw.line(start_x + end_x, path_color, self.line_width)

        for i in range(1, len(path)):
            p1, p2 = path[i-1], path[i]
            d1 = determine_direction(p1, p2)
            d2 = determine_direction(p2, p1)

            start, end = draw_line(p1, d1)
            draw.line(start + end, path_color, self.line_width)
            start, end = draw_line(p2, d2)
            draw.line(start + end, path_color, self.line_width)

    def save_as(self, image_name: str):
        self.drawing_surface.save(image_name)

    def solve_and_save_as(self, image_name: str, path_color: tuple = (255, 0, 0)):
        path = self.maze.to_graph().find_path(self.maze.start, self.maze.end)
        self.draw_path(path, path_color)
        self.save_as(image_name)
