from settings import *
from cell import Cell
import pygame as pg
import numpy as np
import json
import sys


class Main:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.grid = []
        self.stack = []
        # Create cells
        for col in range(COLS):
            for row in range(ROWS):
                cell = Cell(col, row)
                self.grid.append(cell)
        self.current = self.grid[0]

    def run(self):
        """Maze Generator run loop"""
        self.events()
        self.updates()
        self.draw()
        self.clock.tick(FPS)

    def events(self):
        """Check if exit window"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.save_cells()
                elif event.key == pg.K_l:
                    self.load_cells()

    def updates(self):
        # Sets current cell to visited
        self.current.visited = True
        # Picks random neighbor
        nxt = self.current.check_neighbors(self.grid)
        if nxt:
            nxt.visited = True
            # Pushes current cell to stack
            self.stack.append(self.current)
            self.current.in_stack = True
            # Removes walls of both cells
            remove_walls(self.current, nxt)
            # Moves neighbor to current
            self.current = nxt
        elif len(self.stack) > 0:
            self.current = self.stack[-1]
            self.stack.remove(self.current)
            self.current.in_stack = False

    def draw(self):
        """Draws to screen"""
        self.screen.fill(BLACK)
        # Draws wall lines
        for cell in self.grid:
            cell.show(self.screen)
        # Highlights current cell in blue
        self.current.highlight(self.screen)
        pg.display.flip()

    def load_cells(self):
        """Loads cells from a json file"""
        with open('cells.json') as file:
            cells = json.load(file)
            g_counter = 0
            for walls in cells['cells']:
                self.grid[g_counter].set_walls(walls)
                self.grid[g_counter].visited = True
                g_counter += 1
        print('----loaded----')

    def save_cells(self):
        """Saves the list of cells to a json when the maze is finished"""
        maze = {'cells': [cell.walls for cell in self.grid]}
        with open('cells.json', 'w') as file:
            json.dump(maze, file)
        print('-----saved-----')


def remove_walls(a, b):
    """Removes walls from a and b, considering they're both cells"""
    x = a.column - b.column
    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False
    y = a.row - b.row
    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False


m = Main()
while m.running:
    m.run()
