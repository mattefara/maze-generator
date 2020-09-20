from .graph import Graph
from random import randint, choice


class Maze:
    class Room:
        class Type:
            RESET, NOT_VISITED, VISITED, WALL, END_POINT, PATH = -1, 0, 1, 2, 3, 4

        class Side:
            TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3

        def __init__(self, position, room_type):
            self.room_type = room_type
            self.y, self.x = position
            self.sides = {
                Maze.Room.Side.TOP: True,
                Maze.Room.Side.RIGHT: True,
                Maze.Room.Side.BOTTOM: True,
                Maze.Room.Side.LEFT: True,
            }

        def get_position(self):
            return (self.y, self.x)

        def neighbourns(self, ignore: bool = True):

            for side, value in self.__iter__():
                if ignore or value == False:
                    if side == Maze.Room.Side.TOP:
                        yield self.y - 1, self.x
                    if side == Maze.Room.Side.RIGHT:
                        yield self.y, self.x + 1
                    if side == Maze.Room.Side.BOTTOM:
                        yield self.y + 1, self.x
                    if side == Maze.Room.Side.LEFT:
                        yield self.y, self.x - 1

        def get_side(self, side_name):
            return self.sides[side_name]

        def set_side(self, side_name, value):
            self.sides[side_name] = value

        def change_sides(self, next_room=None):
            if next_room is None:
                return next_room
            y, x = self.get_position()
            next_y, next_x = next_room.get_position()
            if y == next_y:
                if x < next_x:  # GO RIGHT
                    next_room.set_side(Maze.Room.Side.LEFT, False)
                    self.set_side(Maze.Room.Side.RIGHT, False)
                else:  # GO LEFT
                    next_room.set_side(Maze.Room.Side.RIGHT, False)
                    self.set_side(Maze.Room.Side.LEFT, False)
            else:
                if y > next_y:  # GO UP
                    next_room.set_side(Maze.Room.Side.BOTTOM, False)
                    self.set_side(Maze.Room.Side.TOP, False)
                else:  # GO DOWN
                    next_room.set_side(Maze.Room.Side.TOP, False)
                    self.set_side(Maze.Room.Side.BOTTOM, False)
            return next_room

        def __iter__(self):
            for side in self.sides:
                yield side, self.sides[side]

        def __repr__(self):
            switch = {
                Maze.Room.Type.NOT_VISITED: "NOT_VISITED",
                Maze.Room.Type.VISITED: "VISITED",
                Maze.Room.Type.WALL: "WALL",
                Maze.Room.Type.END_POINT: "END_POINT",
                Maze.Room.Type.PATH: "PATH",
                Maze.Room.Type.RESET: "RESET",
            }
            return f'x = {self.x},  y = {self.y}: {switch[self.room_type]}, {self.sides}'

    def __init__(self, maze_size, start_position=(-1, 1), end_position=(-1, 1)):
        self.rows, self.cols = maze_size
        self.start = start_position
        self.end = end_position
        self.rooms = []
        self.fill_rooms(Maze.Room.Type.NOT_VISITED)

    def fill_rooms(self, room_type):
        for row in range(self.rows):
            self.rooms.append(
                [Maze.Room((row, col), Maze.Room.Type.NOT_VISITED) for col in range(self.cols)])

    def get_room(self, coordinates: tuple):
        row, col = coordinates
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return self.rooms[row][col]
        return None

    def get_neighbourns(self, position, callback_condition, ignore_wall: bool = True) -> list:
        room = self.get_room(position)
        neighbourns = []
        for y, x in room.neighbourns(ignore_wall):
            current = self.get_room((y, x))
            if current is not None and (callback_condition(current)):
                neighbourns.append(current)
        return neighbourns

    def set_room_type(self, room, room_type):
        if room.room_type < room_type or room_type < 0:
            room.room_type = room_type

    def generate(self):
        self.start = 0, randint(0, self.cols - 1)
        self.end = self.rows - 1, randint(0, self.cols - 1)
        print(f'End at {self.end}. Start at {self.start}')

        self.set_room_type(self.get_room(self.start), Maze.Room.Type.END_POINT)
        self.get_room(self.start).set_side(Maze.Room.Side.TOP, False)

        def build_maze(coordinates: tuple):

            def is_visited(current) -> bool:
                return current.room_type == Maze.Room.Type.NOT_VISITED

            def is_visited_or_end_point(current) -> bool:
                return current.room_type == Maze.Room.Type.VISITED or current.room_type == Maze.Room.Type.END_POINT

            to_visit_stack = []
            # set current room visited
            current_room = self.get_room(coordinates)
            self.set_room_type(current_room, Maze.Room.Type.VISITED)

            # adding current neighbors to to_visit_stack
            current_neighbors = self.get_neighbourns(
                current_room.get_position(), is_visited)
            to_visit_stack += current_neighbors

            while len(to_visit_stack) > 0:
                # select random index from to_visit_stack
                selected_index = randint(0, len(to_visit_stack) - 1)

                next_room = to_visit_stack.pop(selected_index)
                # print(f'Current room = {current_room}, selecting index: {selected_index}, next room = {next_room}')

                visited_neighbourns = self.get_neighbourns(
                    next_room.get_position(), is_visited_or_end_point)
                chosen_neighborn = choice(visited_neighbourns)

                next_room.change_sides(chosen_neighborn)
                self.set_room_type(next_room, Maze.Room.Type.VISITED)

                current_neighbors = self.get_neighbourns(next_room.get_position(
                ), lambda current: current.room_type == Maze.Room.Type.NOT_VISITED)
                for neighborn in current_neighbors:
                    if neighborn not in to_visit_stack:
                        # print(f'Adding {neighborn}')
                        to_visit_stack += [neighborn]
                current_room = next_room

            self.set_room_type(self.get_room(self.end),
                               Maze.Room.Type.END_POINT)
            self.get_room(self.end).set_side(Maze.Room.Side.BOTTOM, False)
        build_maze(self.start)

    def to_graph(self) -> Graph:
        maze_graph = Graph()
        start = self.start

        def pick(current):
            return current.room_type != Maze.Room.Type.PATH or current.room_type == Maze.Room.Type.END_POINT

        stack = [start]
        # Start node
        maze_graph.add_node(Graph.Node(start, ''))

        while len(stack) > 0:

            current_position = stack.pop()
            self.set_room_type(self.get_room(
                current_position), Maze.Room.Type.PATH)
            neighbourns = self.get_neighbourns(
                current_position, pick, ignore_wall=False)
            for neighborn in neighbourns:
                next_position = neighborn.get_position()
                self.set_room_type(neighborn, Maze.Room.Type.PATH)
                current_node = maze_graph.get_node(current_position)
                next_node = Graph.Node(next_position, '')
                # maze_graph.add_node(current_node)
                maze_graph.add_node(next_node)
                maze_graph.add_arch(current_node, next_node, 1)
                stack += [next_position]

        return maze_graph

    def __iter__(self):
        for row in range(self.rows):
            for col in range(self.cols):
                yield self.get_room((row, col))
