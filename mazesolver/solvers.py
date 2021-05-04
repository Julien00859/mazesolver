#!/usr/bin/env python3

"""
Maze solvers, multiple solutions are proposed, depth-first,
breadth-first and iterative-deepening. Breadth-first finds the shortest
path, depth-first and breadth-first are memory efficient but find a
very long solution.
"""

import itertools
import sys
import fileinput
import time


WIDTH = None
HEIGHT = None
PATH = " "
WALL = "#"
PEBBLE = "."


def depth_first_search(grid, startpos):
    stack = [startpos]

    while stack:
        x, y = curpos = stack[-1]

        if is_at_exit(curpos):
            # Solution found
            return stack

        dire = available_direction(grid, curpos)

        if not dire:
            # Deadend, go back
            stack.pop()
            stack.pop()

        else:
            # At least one direction
            dx, dy = dire
            grid[y + dy][x + dx] = PEBBLE
            grid[y + dy * 2][x + dx * 2] = PEBBLE
            stack.append((x + dx, y + dy))
            stack.append((x + dx * 2, y + dy * 2))

    raise ValueError("Unsolvable maze")


def breadth_first_search(grid, startpos):

    class TreeNode:
        def __init__(self, parent, value):
            self.parent = parent
            self.value = value

    stage = [TreeNode(None, startpos)]

    while stage is not None:
        next_stage = []

        for leaf in stage:
            x, y = curpos = leaf.value

            if is_at_exit(curpos):
                # Solution found
                stack = []
                while leaf is not None:
                    stack.append(leaf.value)
                    leaf = leaf.parent
                stack.reverse()
                return stack

            for dx, dy in iter(lambda: available_direction(grid, curpos), None):
                # Add every possible next position to the next stage
                grid[y + dy][x + dx] = PEBBLE
                grid[y + dy * 2][x + dx * 2] = PEBBLE
                stage.append(
                    TreeNode(
                        TreeNode(leaf, (x + dx, y + dy)),  # The intermediary peddle
                        (x + dx * 2, y + dy * 2)
                    )
                )

        stage = next_state

    raise ValueError("Unsolvable maze")


def iterative_deeping(grid, startpos):
    for maxdepth in itertools.count(start=WIDTH + HEIGHT, step=2):
        grid[startpos[1]][startpos[0]] = PEBBLE
        stack = [startpos, startpos]
        fog = False

        while stack:
            for line in grid:
                print("".join(line[:WIDTH]).replace('#', '▊').replace('.', "\033[1;32m" "\033[1;49m" "+" "\033[0m"))
            time.sleep(0.001)


            x, y = curpos = stack[-1]

            if is_at_exit(curpos):
                # Solution found
                return stack

            dire = available_direction(grid, curpos)

            if not dire:
                # Deadend, go back
                x, y = stack.pop()
                x, y = stack.pop()

            elif len(stack) >= maxdepth:
                # Forbidden to explore further, go back
                fog = True
                x, y = stack.pop()
                x, y = stack.pop()

            else:
                try:
                    # Explore the available direction
                    dx, dy = dire
                    grid[y + dy][x + dx] = PEBBLE
                    grid[y + dy * 2][x + dx * 2] = PEBBLE
                    stack.append((x + dx, y + dy))
                    stack.append((x + dx * 2, y + dy * 2))
                except IndexError:
                    breakpoint()
                    print()

        if not fog:
            # The maze was fully explored
            raise ValueError("Unsolvable maze")

        reset(grid)


def reset(grid):
    for lno in range(len(grid)):
        for cno in range(len(grid[lno])):
            if grid[lno][cno] in (PEBBLE, "+"):
                grid[lno][cno] = PATH

def is_at_exit(pos):
    return pos == (WIDTH, HEIGHT - 2)


def available_direction(grid, pos):
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (  0 <= x + dx < WIDTH
          and 0 <= y + dy < HEIGHT
          and grid[y + dy][x + dx] == PATH):
            return dx, dy


def main():
    global WIDTH, HEIGHT
    grid = [list(line.rstrip('\n')) for line in fileinput.input()]
    if not grid[-1]:
        grid.pop()
    HEIGHT = len(grid)
    WIDTH = len(grid[0])
    grid[-2].append(" ")  # Shhhhhh

    solution = iterative_deeping(grid, (1, 1))
    return
    reset(grid)
    for x, y in solution:
        print(x, y)

    for line in grid:
        print("".join(line[:WIDTH]))


if __name__ == '__main__':
    main()
