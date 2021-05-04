#!/usr/bin/env python3

"""
This program generate a random maze (as a cyclic graph, not a tree).

The generatation starts by filling the space with walls, it then spawn
multiple "turtles" in the maze, each tick the turtles will "eat" two
walls in a direction. The turtles prefer to eat two walls but sometimes
they will eat one wall and end up in a path, connecting multiple path
together.
"""

import sys
from collections import namedtuple
from random import choice, random, randrange, sample, shuffle

CellsAround = namedtuple("CellsAround", ["N", "E", "S", "W"])
WALL = "#"
PATH = " "
TURTLE = "."


class Maze:
    def __init__(self, flatgrid, width, height):
        assert len(flatgrid) == width * height
        self.grid = flatgrid
        self.width = width
        self.height = height

    def _safepos(self, pos):
        x, y = pos
        return (x % self.width, y % self.height)

    def __getitem__(self, pos):
        x, y = self._safepos(pos)
        return self.grid[y * self.width + x]

    def __setitem__(self, pos, elem):
        x, y = self._safepos(pos)
        self.grid[y * self.width + x] = elem

    def __delitem__(self, pos):
        x, y = self._safepos(pos)
        del self.grid[y * self.width + x]


    @classmethod
    def generate(cls, width, height):
        maze = cls([WALL for _ in range(width  * height)], width, height)

        for x in range(0, width):
            maze[x, 0] = PATH
            maze[x, height - 1] = PATH
        for y in range(0, height):
            maze[0, y] = PATH
            maze[width - 1, y] = PATH

        turtles = [
            Turtle(maze, x, y)
            for x in range(32, width, 64)
            for y in range(32, height, 64)
        ]


        while turtles:
            #print(maze)
            for i in range(len(turtles) - 1, -1, -1):
                dideat = turtles[i].eatany()
                if not dideat:
                    del turtles[i]

        for i, cell in enumerate(maze.grid):
            if cell == TURTLE:
                maze.grid[i] = PATH

        maze[2, 2] = TURTLE
        maze[width - 2, height - 3] = PATH

        return maze


    def whatsaround(self, x, y, d=1):
        assert self[x, y] != WALL
        return CellsAround(
            self[x, y - d],  # N
            self[x + d, y],  # E
            self[x, y + d],  # S
            self[x - d, y],  # W
        )

    def __iter__(self):
        for h in range(1, self.height - 1):
            yield "".join(self.grid[1 + h * self.width:(h + 1) * self.width - 1])

    def __str__(self):
        return "\n".join(
                "".join(self.grid[h * self.width:(h + 1) * self.width])
            for h in range(self.height)
        )


class Turtle:
    def __init__(self, maze, x, y):
        self.maze = maze
        self.maze[x, y] = PATH
        self.tail = [(x, y)]

    def eatany(self):
        while self.tail:
            x, y = self.tail[-1]
            d = choice([2])
            cells = self.maze.whatsaround(x, y, d)
            for i in sample(range(4), 4):
                if cells[i] != PATH:
                    dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][i]
                    for i in range(d + 1):
                        self.maze[x + dx * i, y + dy * i] = PATH
                    if random() < .2:
                        self.maze[x, y] = TURTLE
                    self.tail.append((x + dx * 2, y + dy * 2))
                    return True

            if not self.tail:
                return False

            self.x, self.y = self.tail.pop()



if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        sys.exit(f"usage: {sys.executable} {sys.argv[0]} <width> <height>")

    width = int(sys.argv[1])
    height = int(sys.argv[2])

    maze = Maze.generate(width, height)

    for line in maze:
        sys.stdout.write(line)
        sys.stdout.write("\n")
